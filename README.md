# TruckProject Django Backend 

**Parent URL:-** http://43.205.91.117:8000/ <br>
* **register:** <br>
**URL:** /api/user/register/ <br>
**Method:** POST <br>
**Body Content:** { <br>
&emsp; &emsp;    "email":, <br>
&emsp; &emsp;    "first_name": , <br>
&emsp; &emsp;    "last_name": , <br>
&emsp; &emsp;    "phone_number": , <br>
&emsp; &emsp;    "password": , <br>
&emsp; &emsp;    "password2": <br>
&emsp; &emsp;}


* **verify_otp:** <br>
**URL:** /api/user/verify_otp/ <br>
**Method:** POST <br>
**Body Content:** { <br>
&emsp; &emsp;	‘otp’: <br>
}

* **resend otp:** <br>
**URL:** /api/user/resend_otp/ <br>
**Method:** GET

* **Login:** <br>
**URL:** /api/user/login/ <br>
**Method:** POST <br>
**Body Content:** <br>
{ <br>
&emsp; &emsp;    "email":, <br>
&emsp; &emsp;    "password": <br>
}

* **Change Password:** <br>
**Objective:** When the current password is known but the user still wishes to change it. <br>
**URL:** /api/user/changepassword/ <br>
**Method:** POST <br>
**Body Content:** <br> 
{ <br>
&emsp; &emsp;    "password": , <br>
&emsp; &emsp;    "Password2":   // this will be the new password and confirm password <br>
} <br>
**Header:** <br>
{
&emsp; &emsp; **Accept:** application/json <br>
&emsp; &emsp; **Authorization:** Bearer {token} <br>
}

* **Send Email Reset Password:** <br>
**URL:** /api/user/send-reset-password-email/ <br>
**Objective:** Will send email having the link to reset the password. <br>
**Body:** <br>
{ <br>
&emsp; &emsp;    "email": <br>
} <br>
**Method:** POST

* **Reset Password:** <br>
This should activate after clicking on the link sent through mail. <br>
**URL:** /api/user/reset-password/{user_id}/{token}/ <br>
**Method:** POST <br>
**Body:** <br>
{ <br>
&emsp; &emsp;    "password": , <br>
&emsp; &emsp;    "password2":  <br>
}

* **text_rekognition:** <br>
**URL:** /api/text_rekognition/ <br>
**Method:** POST <br>
**Body:** <br>
{ <br>
&emsp; &emsp; ‘picture’ : {ImageFile} <br>
}

* **entry_datetime:** <br>
**URL:** /api/entry_datetime/{truck_id}/ <br>
**Method:** GET <br>
**Objective:** Will give Entry date and entry time of the corresponding truck_id passed in URL 

* **latest_truck_entered:** <br>
**URL:** /api/latest_truck_entered/ <br>
**Method:** GET <br>
**Objective:** Will give truck_id of the truck entered recently

* **exit_time:** <br>
**URL:** /api/exit_time/{truck_id}/ <br>
**Method:** GET <br>
**Objective:** Will give exit time of the corresponding truck_id

* **trucks_inside:** <br>
**URL:** /api/trucks_inside/ <br>
**Method:** GET <br>
**Objective:** Will return number of trucks inside and all their details

* **insert_sku_details:** <br>
**URL:** /api/user/insert_sku_details/ <br>
**Method:** POST <br>
**Objective:** Will insert details of all the SKUs in a truck <br>
**Body:** <br>
{ <br>
&emsp; &emsp; ‘Sku’: <br>
&emsp; &emsp; ‘truck’: <br>
&emsp; &emsp; ‘quantity’: <br>
}

* **sku_details:** <br>
**URL:** /api/user/sku_details/{truck_id} <br>
**Objective:** Will give details of all the SKUs in the corresponding truck_id. <br>
**Method:** GET

* **update_api:** <br>
**Method:** PATCH <br>
**URL:** /api/update_status/{truck_id} <br>
**Objective:** Will update loading status for corresponding truck_id. <br>
**Body:** <br>
{ <br>
&emsp; &emsp; ‘status’ : “Loading/Unloading” <br>
}

* **Phone validation api:** <br>
**Method:** POST <br>
**URL:** /api/user/phone_validation/ <br>
**Objective:** If a user tries to login but its phone number is not verified then this API will be used to direct to the next page, so that user could verify his phone number only. <br>
**Body:** <br>
{ <br>
&emsp; &emsp;	‘phone’:  <br>
}

* **Resend Email:** <br>
**Method:** POST <br>
**URL:** /api/user/resend_email/ <br>
**Objective:** If the user's mail id is not verified then the user will be asked to enter his email and will receive the verification link again, clicking on which the email will be verified. <br>
**Body:** <br>
{ <br>
&emsp; &emsp; ‘email’ : <br>
}

<br> <br>
Note: **To change the model path, move to DjangoAPIs/model/sample.py**