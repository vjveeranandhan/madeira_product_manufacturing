import re
from .models import CustomUser

def validate_user_data(data, activity):
    phone_number_pattern = r'^[6-9]\d{9}$'
    phone_number_regex = re.compile(phone_number_pattern)
    try:
        min_length = 8
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

        if 'name' in data:
            if data['name'] is None:
                return False, "Name should not be Null!"
        else:
            return False, "Name field is missing!"
        
        if 'age' in data:
            if data['age'] is None:
                return False, "Age should not be Null!"
        else:
            return False, "Age field is missing!"
        
        if 'phone' in data:
            if data['phone'] is not None:
                if activity == 'user-update':
                    if phone_number_regex.match(data['phone']):
                        if CustomUser.objects.filter(phone= data['phone']).exclude(id=data['id']).exists():
                            return False, "Phone number alrady exists!"
                    else:
                        return False, "Invalid phone number!"
                else:
                    if CustomUser.objects.filter(phone= data['phone']).exists():
                        return False, "Phone number alrady exists!"
            else:
                return False, "Phone Number should not be Null!"
        if 'email' in data:
            if data['email'] is not None:
                if CustomUser.objects.filter(email= data['email'] ).exists():
                    return False, "Email alrady exists!"
            else:
                return False, "Email should not be Null!"
        else:
            return False, "Email is missing!"
        if 'password' in data:
            if data['password'] is None:
                return False, "Password should not be Null!"
        else:
            return False, "Password field is missing!"
        if 'isAdmin' in data:
            if data['isAdmin'] is None:
                return False, "isAdmin should not be Null!"
        else:
            return False, "isAdmin field is missing!"
        return True, "Valid."
    except:
        return False, "Something went wrong. Please Try agan later."

    # try:
    #     min_length = 8
    #     regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    #     if activity == 'user-update':
    #         if 'id' not in data:
    #             return False, "User id missing!"
    #     if 'first_name' in data:
    #         if data['first_name'] is None:
    #             return False, "First name should not be Null!"
    #     if 'last_name' in data:
    #         if data['last_name'] is None:
    #             return False, "Last name should not be Null!"
    #     if 'email' in data:
    #         if data['email'] is not None:
    #             if activity == 'user-update':
    #                 if CustomUser.objects.filter(email= data['email'] ).exclude(id=data['id']).exists():
    #                     return False, "Email alrady exists!"
    #             else:
    #                 if CustomUser.objects.filter(email= data['email'] ).exists():
    #                     return False, "Email alrady exists!"
    #         else:
    #             return False, "Email should not be Null!"
    #         data['username'] = data['email']
    #     else:
    #         return False, "Email is missing!"
    #     if 'phone' in data:
    #         if data['phone'] is not None:
    #             if activity == 'user-update':
    #                 if phone_number_regex.match(data['phone']):
    #                     if CustomUser.objects.filter(phone= data['phone']).exclude(id=data['id']).exists():
    #                         return False, "Phone number alrady exists!"
    #                 else:
    #                     return False, "Invalid phone number!"
    #             else:
    #                 if CustomUser.objects.filter(phone= data['phone']).exists():
    #                     return False, "Phone number alrady exists!"
    #         else:
    #             return False, "Phone Number should not be Null!"
    #     else:
    #         return False, "Phone number is missing!"
    #     if 'dateofbirth' in data:
    #         if data['dateofbirth'] is None:
    #             return False, "Date of Birth is missing!"
    #     if activity == 'user-creation':
    #         if len(data['password']) < min_length:
    #             return False, f"Password must be at least {min_length} characters long."
    #         if not re.match(regex, data['password']):
    #             return False, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
    #         if data['password'] != data['confirm_password']:
    #             return False, "Passwords do not match."
    #     return True, "Valid."
    # except:
    #     return False, "Something went wrong. Please Try agan later."
