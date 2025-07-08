import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from signup.models import Staff
from django.contrib.auth.hashers import make_password

verification_code = {}  # bạn có thể dùng session hoặc dict toàn cục cho demo

def index(request):
    return render(request, "forgotpassword/forgotpassword.html")

def send_test_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        code = random.randint(100000, 999999)
        
        subject = "Xác nhận quên mật khẩu qua mail"
        message = f"Chào {first_name},\n\nMã xác nhận của bạn là: {code}\n\nThân mến!"
        recipient_list = [email]

        try:
            staff = Staff.objects.get(email=email, first_name=first_name)
        except Staff.DoesNotExist:
            messages.error(request, "❌ Email hoặc tên không khớp.")
        
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        messages.success(request, "✅ Mã xác nhận đã được gửi đến email!")
        return redirect("forgotpassword:confirm_code") 

    else:
        return render(request, "forgotpassword/forgotpassword.html")

def confirm_code(request):
    return render(request, 'forgotpassword/verification_code.html')


'''def confirm_code(request):
    email = request.session.get('email')  # email lưu từ bước trước khi gửi OTP
    message = ''
    success = False
    allow_password_change = False

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'verify':
            otp = request.POST.get('otp')
            if verification_code.get(email) == otp:
                message = '✅ Mã xác nhận đúng. Bạn có thể đổi mật khẩu.'
                success = True
                allow_password_change = True
                request.session['verified'] = True
            else:
                message = '❌ Mã xác nhận không đúng. Vui lòng thử lại.'
        elif action == 'change_password' and request.session.get('verified'):
            new_password = request.POST.get('new_password')
            try:
                user = Staff.objects.get(email=email)
                user.password = make_password(new_password)  # mã hóa mật khẩu
                user.save()
                del request.session['verified']
                message = '✅ Đổi mật khẩu thành công.'
                success = True
                return redirect('login')  # chuyển về trang đăng nhập
            except Staff.DoesNotExist:
                message = '❌ Không tìm thấy tài khoản.'
    
    allow_password_change = request.session.get('verified', False)
    return render(request, 'forgotpassword/confirm_code.html', {
        'message': message,
        'success': success,
        'allow_password_change': allow_password_change,
    })'''
