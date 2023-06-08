import streamlit as st
st.set_page_config(
	page_icon = "🤗",
	page_title = "파이썬 웹앱",
	)

view = [10,20,30,40,50]
st.write('# Data Chart')
st.write('## raw data')
view
st.write('## bar chart')
st.bar_chart(view)


st.write('## 일별 인구수')
cols = st.columns((1,1,2))
cols[0].metric("6/1", "10,000명", "10")
cols[0].metric("6/2", "10,020명", "20")
cols[0].metric("6/3", "10,010명", "-10")
cols[1].metric("6/4", "10,005명", "-5")
cols[1].metric("6/5", "10,035명", "30")
cols[1].metric("6/6", "9,935명", "-100")

cols[2].bar_chart(view)


import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")

if uploaded_file is not None:
    # 업로드된 CSV 파일을 DataFrame으로 읽기
    df = pd.read_csv(uploaded_file)

    # 차트 유형 선택
    chart_type = st.selectbox("차트 유형 선택", ["선 그래프", "막대 그래프"])

    if chart_type == "선 그래프":
        # X, Y축 선택
        x_col = st.selectbox("X축 선택", df.columns)
        y_cols = st.multiselect("Y축 선택", df.columns)

        # X축 최소값과 최대값 입력
        x_min = st.number_input("X축 최소값", value=df[x_col].min())
        x_max = st.number_input("X축 최대값", value=df[x_col].max())

        # Y축 최소값과 최대값 입력
        y_min = st.number_input("Y축 최소값", value=int(df[y_cols].values.min()))
        y_max = st.number_input("Y축 최대값", value=int(df[y_cols].values.max()))


        # 선택한 열의 데이터로 선 그래프 그리기
        for col in y_cols:
            plt.plot(df[x_col], df[col])

        # 축 범위 설정
        plt.ylim(y_min, y_max)

        # 그래프 출력
        st.pyplot()

    elif chart_type == "막대 그래프":
        # X, Y축 선택
        x_col = st.selectbox("X축 선택", df.columns)
        y_col = st.selectbox("Y축 선택", df.columns)

        # X축 Y축 최소값과 최대값 입력
        x_min, x_max = st.slider("X축 범위", int(df[x_col].min()), int(df[x_col].max()), value=(int(df[x_col].min()), int(df[x_col].max())))
        y_min, y_max = st.slider("Y축 범위", int(df[y_col].min()), int(df[y_col].max()), value=(int(df[y_col].min()), int(df[y_col].max())))

        # 그래프 색상 선택
        line_color = st.color_picker("선 그래프 색상 선택")

        # 선택한 열의 데이터로 막대 그래프 그리기
        plt.bar(df[x_col], df[y_col], color=line_color)

        # 축 범위 설정
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)

        # 그래프 출력
        st.pyplot()


html_code = """
<div>사람과 손 구별</div>
<button type="button" onclick="init()">시작하기</button>
<div id="webcam-container"></div>
<div id="label-container"></div>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"></script>
<script type="text/javascript">
    // More API functions here:
    // https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/image

    // the link to your model provided by Teachable Machine export panel
    const URL = "https://teachablemachine.withgoogle.com/models/p4qvyuARV/";

    let model, webcam, labelContainer, maxPredictions;

    // Load the image model and setup the webcam
    async function init() {
        const modelURL = URL + "model.json";
        const metadataURL = URL + "metadata.json";

        // load the model and metadata
        // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
        // or files from your local hard drive
        // Note: the pose library adds "tmImage" object to your window (window.tmImage)
        model = await tmImage.load(modelURL, metadataURL);
        maxPredictions = model.getTotalClasses();

        // Convenience function to setup a webcam
        const flip = true; // whether to flip the webcam
        webcam = new tmImage.Webcam(200, 200, flip); // width, height, flip
        await webcam.setup(); // request access to the webcam
        await webcam.play();
        window.requestAnimationFrame(loop);

        // append elements to the DOM
        document.getElementById("webcam-container").appendChild(webcam.canvas);
        labelContainer = document.getElementById("label-container");
        for (let i = 0; i < maxPredictions; i++) { // and class labels
            labelContainer.appendChild(document.createElement("div"));
        }
    }

    async function loop() {
        webcam.update(); // update the webcam frame
        await predict();
        window.requestAnimationFrame(loop);
    }

    // run the webcam image through the image model
    async function predict() {
        // predict can take in an image, video or canvas html element
        const prediction = await model.predict(webcam.canvas);
        for (let i = 0; i < maxPredictions; i++) {
            const classPrediction =
                prediction[i].className + ": " + prediction[i].probability.toFixed(2);
            labelContainer.childNodes[i].innerHTML = classPrediction;
        }
    }
</script>
"""

st.components.v1.html(html_code,height=300)