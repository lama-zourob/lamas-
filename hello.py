from flask import Flask, request, render_template  
app=Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def calculate():
    num1 = request.form['num1']
    num2 = request.form['num2']
    operation = request.form['operation']
    if operation=='add':
         result = int(num1) + int(num2)
         return render_template('sw.html', result=result)
    elif operation=='subtract':
         result=int(num1)-int(num2)
         return render_template('sw.html', result=result)

    
    return render_template('sw.html')

if __name__ == '__main__':
    app.run(debug=True)


