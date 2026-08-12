from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import (
    Alert,
    EmergencyResource,
    HelpRequest,
    UserProfile
)

from .forms import (
    AlertForm,
    HelpRequestUpdateForm
)

from .utils import send_sms




def home(request):

   
    alerts = Alert.objects.all().order_by(
        "-alert_date"
    )[:3]

    return render(
        request,
        "home.html",
        {
            "alerts": alerts
        }
    )




def register(request):

    # Already logged-in users should not register again
    if request.user.is_authenticated:

        # Redirect according to role
        if request.user.is_superuser:
            return redirect("admin_dashboard")

        try:

            if request.user.userprofile.role == "COORDINATOR":
                return redirect("coordinator_dashboard")

        except UserProfile.DoesNotExist:
            pass

        return redirect("dashboard")


    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )


  

        if not username or not email or not phone or not password:

            messages.error(
                request,
                "Please fill in all required fields."
            )

            return redirect("register")


       

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("register")


       

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")


       

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email already registered."
            )

            return redirect("register")


      

        user = User.objects.create_user(

            username=username,

            email=email,

            password=password

        )


    

        UserProfile.objects.create(

            user=user,

            phone=phone,

            role="USER"

        )


        messages.success(

            request,

            "Registration successful. Please login."

        )


        return redirect(
            "login"
        )


    return render(

        request,

        "register.html"

    )




def user_login(request):

    # Already logged-in user
    if request.user.is_authenticated:

        if request.user.is_superuser:

            return redirect(
                "admin_dashboard"
            )


        try:

            if request.user.userprofile.role == "COORDINATOR":

                return redirect(
                    "coordinator_dashboard"
                )

        except UserProfile.DoesNotExist:

            pass


        return redirect(
            "dashboard"
        )


    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )


      

        user = authenticate(

            request=request,

            username=username,

            password=password

        )


        if user is None:

            messages.error(

                request,

                "Invalid username or password."

            )

            return redirect(
                "login"
            )


    

        login(

            request,

            user

        )


        messages.success(

            request,

            "Login successful."

        )


     

        if user.is_superuser:

            return redirect(
                "admin_dashboard"
            )


   

        try:

            if user.userprofile.role == "COORDINATOR":

                return redirect(
                    "coordinator_dashboard"
                )


        except UserProfile.DoesNotExist:

            # If profile is missing,
            # create a normal user profile.

            UserProfile.objects.create(

                user=user,

                phone="",

                role="USER"

            )


     

        return redirect(
            "dashboard"
        )


    return render(

        request,

        "login.html"

    )




@login_required
def user_logout(request):

    logout(
        request
    )

    messages.success(

        request,

        "Logged out successfully."

    )

    return redirect(
        "home"
    )




def is_coordinator(user):

    # Must be logged in
    if not user.is_authenticated:

        return False


    # Admin is also technically allowed
    # for internal permission checks

    if user.is_superuser:

        return True


    try:

        return (

            user.userprofile.role

            == "COORDINATOR"

        )


    except UserProfile.DoesNotExist:

        return False



def is_normal_user(user):

    if not user.is_authenticated:

        return False


    # Admin is not a normal user

    if user.is_superuser:

        return False


    try:

        return (

            user.userprofile.role

            == "USER"

        )


    except UserProfile.DoesNotExist:

        return False




@login_required
def dashboard(request):



    if request.user.is_superuser:

        return redirect(
            "admin_dashboard"
        )


 

    try:

        if request.user.userprofile.role == "COORDINATOR":

            return redirect(
                "coordinator_dashboard"
            )


    except UserProfile.DoesNotExist:

        messages.error(

            request,

            "User profile not found."

        )

        return redirect(
            "home"
        )




    alerts = Alert.objects.all().order_by(

        "-alert_date"

    )


   

    resources = EmergencyResource.objects.all()


 

    district = request.GET.get(

        "district"

    )



    resource_type = request.GET.get(

        "resource_type"

    )


    if district:

        resources = resources.filter(

            district__icontains=district

        )


    if resource_type:

        resources = resources.filter(

            resource_type=resource_type

        )


  

    my_requests = HelpRequest.objects.filter(

        user=request.user

    ).order_by(

        "-request_date"

    )[:5]


  

    context = {

        "alerts": alerts,

        "resources": resources,

        "my_requests": my_requests,

    }


    return render(

        request,

        "dashboard.html",

        context

    )




@login_required
def request_help(request):

  

    if request.user.is_superuser:

        return redirect(
            "admin_dashboard"
        )


  

    try:

        if request.user.userprofile.role == "COORDINATOR":

            return redirect(
                "coordinator_dashboard"
            )


    except UserProfile.DoesNotExist:

        pass


    if request.method == "POST":

        phone = request.POST.get(

            "phone",

            ""

        ).strip()


        location = request.POST.get(

            "location",

            ""

        ).strip()


        emergency_type = request.POST.get(

            "emergency_type",

            ""

        )


        description = request.POST.get(

            "description",

            ""

        ).strip()




        if (
            not phone
            or not location
            or not emergency_type
            or not description
        ):

            messages.error(

                request,

                "Please fill in all fields."

            )

            return redirect(

                "request_help"

            )


       

        HelpRequest.objects.create(

            user=request.user,

            phone=phone,

            location=location,

            emergency_type=emergency_type,

            description=description,

            status="Received"

        )


        messages.success(

            request,

            "Emergency help request submitted successfully."

        )


        return redirect(

            "my_requests"

        )


    return render(

        request,

        "request_help.html"

    )




@login_required
def my_requests(request):

    # Admin should not access this page
    if request.user.is_superuser:

        return redirect(
            "admin_dashboard"
        )


    # Coordinator should not access this page
    try:

        if request.user.userprofile.role == "COORDINATOR":

            return redirect(
                "coordinator_dashboard"
            )

    except UserProfile.DoesNotExist:

        pass




    requests = HelpRequest.objects.filter(

        user=request.user

    ).order_by(

        "-request_date"

    )


    return render(

        request,

        "requests.html",

        {

            "requests": requests

        }

    )




@login_required
def admin_dashboard(request):

   

    if not request.user.is_superuser:

        messages.error(

            request,

            "Only the administrator can access this page."

        )

        return redirect(
            "dashboard"
        )




    if request.method == "POST":

        form = AlertForm(

            request.POST

        )


        if form.is_valid():

   

            alert = form.save(

                commit=False

            )


            # Store admin who created alert
            alert.created_by = request.user


            alert.save()


       

            message = (

                f"🚨 Emergency Alert!\n\n"

                f"Disaster: "
                f"{alert.disaster_type}\n"

                f"Area: "
                f"{alert.area}\n\n"

                f"Message: "
                f"{alert.alert_message}"

            )


            

            users = UserProfile.objects.all()


            sms_sent = 0

            sms_failed = 0


      

            for user_profile in users:

                if user_profile.phone:

                    try:

                        send_sms(

                            user_profile.phone,

                            message

                        )

                        sms_sent += 1


                    except Exception as e:

                        print(

                            "SMS Error:",

                            e

                        )

                        sms_failed += 1


            messages.success(

                request,

                f"Alert created successfully. "
                f"SMS sent: {sms_sent}. "
                f"SMS failed: {sms_failed}."

            )


            return redirect(

                "admin_dashboard"

            )


    else:

        form = AlertForm()


   

    # All alerts
    alerts = Alert.objects.all().order_by(

        "-alert_date"

    )


    # Statistics

    total_users = User.objects.count()


    total_alerts = Alert.objects.count()


    total_resources = EmergencyResource.objects.count()


    pending_requests = HelpRequest.objects.filter(

        status="Received"

    ).count()


    total_requests = HelpRequest.objects.count()


    completed_requests = HelpRequest.objects.filter(

        status="Completed"

    ).count()


  

    context = {

        "form": form,

        "alerts": alerts,

        "total_users": total_users,

        "total_alerts": total_alerts,

        "total_resources": total_resources,

        "pending_requests": pending_requests,

        "total_requests": total_requests,

        "completed_requests": completed_requests,

    }


    return render(

        request,

        "admin_dashboard.html",

        context

    )




@login_required
def coordinator_dashboard(request):

   

    if not is_coordinator(

        request.user

    ):

        messages.error(

            request,

            "You are not authorized to access "
            "the coordinator dashboard."

        )


        # Admin goes to admin dashboard
        if request.user.is_superuser:

            return redirect(

                "admin_dashboard"

            )


        # Normal user goes to user dashboard
        return redirect(

            "dashboard"

        )


    

    help_requests = HelpRequest.objects.all().order_by(

        "-request_date"

    )


 

    total_requests = HelpRequest.objects.count()


    received_requests = HelpRequest.objects.filter(

        status="Received"

    ).count()


    in_process_requests = HelpRequest.objects.filter(

        status="In Process"

    ).count()


    completed_requests = HelpRequest.objects.filter(

        status="Completed"

    ).count()


   
    context = {

        "help_requests": help_requests,

        "total_requests": total_requests,

        "received_requests": received_requests,

        "in_process_requests": in_process_requests,

        "completed_requests": completed_requests,

    }


    return render(

        request,

        "coordinator_dashboard.html",

        context

    )




@login_required
def update_help_request(

    request,

    pk

):

    # -----------------------------------------------------
    # ONLY COORDINATOR CAN UPDATE
    # -----------------------------------------------------

    if not is_coordinator(

        request.user

    ):

        messages.error(

            request,

            "You are not authorized to update "
            "emergency requests."

        )


        if request.user.is_superuser:

            return redirect(

                "admin_dashboard"

            )


        return redirect(

            "dashboard"

        )


    # -----------------------------------------------------
    # GET REQUEST
    # -----------------------------------------------------

    help_request = get_object_or_404(

        HelpRequest,

        pk=pk

    )


    # -----------------------------------------------------
    # UPDATE REQUEST
    # -----------------------------------------------------

    if request.method == "POST":

        form = HelpRequestUpdateForm(

            request.POST,

            instance=help_request

        )


        if form.is_valid():

            help_request = form.save(

                commit=False

            )


            # ---------------------------------------------
            # STORE COORDINATOR
            # ---------------------------------------------

            help_request.handled_by = request.user


            # ---------------------------------------------
            # IF COMPLETED
            # ---------------------------------------------

            if help_request.status == "Completed":

                help_request.completed_date = timezone.now()


            else:

                help_request.completed_date = None


            help_request.save()


            messages.success(

                request,

                "Emergency request updated successfully."

            )


            return redirect(

                "coordinator_dashboard"

            )


    else:

        form = HelpRequestUpdateForm(

            instance=help_request

        )


    return render(

        request,

        "update_help_request.html",

        {

            "form": form,

            "help_request": help_request

        }

    )