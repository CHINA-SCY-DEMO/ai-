# 文件名：tianjin_travel_app.py
import streamlit as st
from openai import OpenAI
import pandas as pd

def create_prompt_from_features(user_features):
    """将用户特征转换为结构化的提示文本"""
    prompt = f"""
基于以下用户特征推荐天津旅游景点：
- 年龄段：{user_features['年龄']}
- 同行类型：{user_features['同行人员类型']}
- 预算：{user_features['预算范畴']}
- 计划游玩天数：{user_features['计划游玩天数']}
- 兴趣偏好：{user_features['兴趣标签']}

请根据这些特征推荐最适合的天津旅游景点，并说明推荐理由。
"""
    return prompt

def get_recommendations_from_api(user_features):
    """调用 DeepSeek API 获取推荐结果"""
    try:
        client = OpenAI(
            api_key="sk-27b8b33f6992459781376daecc495bde",
            base_url="https://api.deepseek.com"
        )
        
        # 构建提示文本
        prompt = create_prompt_from_features(user_features)
        
        # 调用API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的天津旅游推荐助手，基于用户特征提供个性化的景点推荐。"},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"API调用错误: {str(e)}"

# 网页界面
st.title("🎯 天津旅游智能推荐系统")

# 创建表单
with st.form("user_input_form"):
    # 下拉选项配置
    age_options = ['18-25', '26-35', '36-45', '46-55', '56+']
    companion_options = ['朋友团体', '家庭', '情侣', '独自旅行', '商务伙伴']
    budget_options = ['经济型（500-1500）', '标准型（1500-4000）', '豪华型（4000+）']
    days_options = ['1-2天', '3-5天', '5天以上']
    interest_tags = ['历史古迹', '自然风光', '美食体验', '都市购物', '艺术人文', '亲子活动']
    
    # 创建下拉菜单
    age = st.selectbox("年龄阶段", age_options, index=1)
    companion = st.selectbox("同行人员类型", companion_options)
    budget = st.selectbox("预算范围", budget_options)
    days = st.selectbox("计划游玩天数", days_options)
    interests = st.multiselect("兴趣偏好（可多选）", interest_tags, default=['历史古迹', '自然风光'])
    
    # 提交按钮
    submitted = st.form_submit_button("生成推荐方案")
    
    if submitted:
        # 构建用户特征
        user_features = {
            '年龄': age,
            '同行人员类型': companion,
            '预算范畴': budget,
            '计划游玩天数': days,
            '兴趣标签': '┋'.join(interests)  # 保持与示例格式一致
        }
        
        # 获取推荐
        with st.spinner('正在生成个性化推荐...'):
            recommendation = get_recommendations_from_api(user_features)
        
        # 显示结果
        st.subheader("🎉 为您定制的推荐方案")
        st.markdown("---")
        st.markdown(recommendation)
        st.success("推荐生成完成！")

# 侧边栏说明
st.sidebar.markdown("""
### 使用说明
1. 选择您的年龄阶段
2. 选择同行人员类型
3. 选择预算范围
4. 选择计划游玩天数
5. 选择兴趣偏好（可多选）
6. 点击「生成推荐方案」按钮

系统将基于AI算法为您推荐最适合的天津旅游方案！
""")