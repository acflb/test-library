import streamlit as st
import pandas as pd
import numpy as np

# 1. 写个大标题
st.title('我的第一个 AI 数据看板 🎉')

# 2. 加一个侧边栏交互
st.sidebar.header("控制台")
user_name = st.sidebar.text_input("请输入你的名字", "Python 练习生")
line_count = st.sidebar.slider('你想生成多少个数据点？', 10, 100, 50)

# 3. 在主界面展示内容
st.write(f"👋 欢迎你，**{user_name}**！")
st.write("下面是根据你的设置实时生成的图表：")

# 4. 生成假数据 (用到了你之前问的 NumPy!)
# 随机生成 line_count 行，3列的数据
chart_data = pd.DataFrame(
    np.random.randn(line_count, 3),
    columns=['A', 'B', 'C']
)

# 5. 画图 (一行代码搞定)
st.line_chart(chart_data)

# 6. 结尾
if st.button('点击这里庆祝一下'):
    st.balloons()  # 这是一个好玩的特效
