from flask import Flask, render_template, request
from twilio.rest import Client

app = Flask(__name__)
account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

@app.route('/')
def home():
    return render_template('front.html')

@app.route ('/calculate', methods = ['POST', 'GET'])
def calculatebmi():
    BMI = ''
    status = ''
    if request.method =='POST' and 'weight' in request.form and 'height' in request.form:
        body_weight = float(request.form.get('weight'))
        body_height = float(request.form.get('height'))
        phone_number = str(request.form.get('phone'))
        BMI = round(703*body_weight)/(body_height **2)

        if BMI > 0:
            client = Client(account_sid, auth_token)
            if BMI < 18.5:
                status = "You are underweight"
                message = client.messages \
                    .create(
                    body="Based on your BMI, you are underweight. Here is are some tips for you to gain weight: https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/expert-answers/underweight/faq-20058429#:~:text=Eat%20five%20to%20six%20smaller,Try%20smoothies%20and%20shakes.",
                    from_='+18457139503',
                    to= phone_number
                )
            elif BMI >=18.5 and BMI <= 24.9:
                status = "You are healthy"
            elif BMI >=25 and BMI <= 29.9:
                status = "You are overweight"
                message = client.messages \
                    .create(
                    body="Based on your BMI, you are overweight. Here is are some tips for you to reduce weight: https://www.hsph.harvard.edu/obesity-prevention-source/obesity-prevention/",
                    from_='+18457139503',
                    to= phone_number
                )
            else:
                status = "You are obese"
                message = client.messages \
                    .create(
                    body="Based on your BMI, you are overweight. Here is are some tips for you to reduce weight: https://www.mayoclinic.org/diseases-conditions/obesity/diagnosis-treatment/drc-20375749",
                    from_='+18457139503',
                    to= phone_number
                )
            return render_template('end.html', bmi=BMI, status=status)
    else:
        return render_template('front.html')

if __name__ == "main":
    app.run(debug=True)
