from flask import Flask, render_template, request, send_from_directory
import matplotlib.pyplot as plt
import warnings
from CustomELECTRAModel import CustomELECTRAModel
from run_model_electra import predict
# Cấu hình matplotlib sử dụng backend không có GUI
plt.switch_backend('Agg')
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
#----------------------------------------------------------------------------

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    pre_label, probabilities_percentage, probability = None, None, None

    if request.method == 'POST':
        content = request.form['content']
        pre_label, percentages, process_content = predict(content)
        
        percentage_real = percentages.get(0, 0)
        percentage_fake = percentages.get(1, 0)
        probabilities_percentage = [round(percentage_real, 2), round(percentage_fake, 2)]
        
        probability = round(percentage_real, 2) if pre_label == 'Real' else round(percentage_fake, 2)
        print("\n==> Nội dung bài báo:", content)
        print("\n==> Nội dung bài báo xử lý:", process_content)
        print("\n==> Dự đoán:", pre_label)
        print(f"\n==> Xác suất: Tin thật: {percentage_real}% | Tin giả: {percentage_fake}%")

    return render_template(
        'index.html',
        predicted_class=pre_label,
        probability=probability,
        probabilities_percentage=probabilities_percentage
    )

if __name__ == '__main__':
    app.run(debug=True)