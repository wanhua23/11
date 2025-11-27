import time
from .utils import fetch_all, delete, search_sql, insert, put
from flask import request, jsonify
from flask import Blueprint
import os
from openai import OpenAI

#   蓝图对象
restaurants = Blueprint("restaurants", __name__)
ai = Blueprint("ai", __name__)



# 删除餐馆
@restaurants.route("/api/restaurants/<int:restaurant_id>", methods=["DELETE"])
def delt(restaurant_id):
    data_list = search_sql("SELECT * FROM restaurants WHERE id=%s", restaurant_id)
    print("查询结果:", data_list)

    # 检查餐厅是否存在
    if not data_list:
        return jsonify({"status": False, "message": "餐厅未找到"})

    delete("DELETE FROM restaurants WHERE id=%s", restaurant_id)
    return jsonify({"status": True, "message": "删除成功"})


# 更新餐馆信息
@restaurants.route("/api/restaurants/<int:restaurant_id>", methods=["PUT"])
def update_restaurant(restaurant_id):
    try:
        # 获取餐厅数据
        data_list = search_sql(f"SELECT * FROM restaurants WHERE id=%s", restaurant_id)
        # 检查餐厅是否存在
        if not data_list:
            return jsonify({"status": False, "message": "餐厅未找到"})

        restaurant = data_list[0]
        print("餐厅数据:", restaurant)

        data = request.get_json()
        print("接收到的数据:", data)

        # 获取所有字段，包括可选的
        name = data.get("name")
        address = data.get("address")
        phone = data.get("phone")
        cuisine_type = data.get("cuisine_type")
        price_range = data.get("price_range")
        rating = data.get("rating")
        description = data.get("description")
        image_url = data.get("image_url")

        print("接收到的表单数据:", name, address, phone, cuisine_type, price_range, rating, description)

        # 验证必填字段
        if not all([name, address, cuisine_type, rating]):
            return jsonify({"status": False, "message": "名称、地址、菜系类型和评分都是必填的"})

        # 验证评分范围
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 5:
                return jsonify({"status": False, "message": "评分必须在0-5之间"})
        except (ValueError, TypeError):
            return jsonify({"status": False, "message": "评分必须是数字"})

        # 执行更新
        result = put("""
            UPDATE restaurants SET 
                name=%s, 
                address=%s, 
                phone=%s, 
                cuisine_type=%s, 
                price_range=%s, 
                rating=%s, 
                description=%s,
                image_url=%s
            WHERE id=%s
            """, [name, address, phone or "", cuisine_type, price_range or "", rating_float, description or "",
                  image_url or "", restaurant_id])

        return jsonify({"status": True, "message": "修改成功", "data": result})

    except Exception as e:
        print("更新餐厅时出错:", str(e))
        return jsonify({"status": False, "message": f"服务器错误: {str(e)}"})


# 获取单个餐馆
@restaurants.route("/api/restaurants/<int:restaurant_id>", methods=["GET"])
def dan(restaurant_id):
    data_list = search_sql("SELECT * FROM restaurants WHERE id=%s", restaurant_id)
    # 检查餐厅是否存在
    if not data_list:
        return jsonify({"status": False, "message": "餐厅未找到"})

    restaurant = data_list[0]
    return jsonify({"status": True, "message": restaurant})


# 获取餐馆列表
@restaurants.route("/api/restaurants", methods=["GET"])
def lists():
    if request.method == "GET":
        data_list = fetch_all("select * from restaurants")

        if data_list:
            # 确保返回的是列表格式
            return jsonify({"status": True, "message": data_list})
        else:
            # 返回空数组而不是字符串
            return jsonify({"status": True, "message": []})


@restaurants.route("/api/restaurants", methods=["POST"])
def add():
        data = request.get_json()
        print("接收到的数据:", data)

        name = data.get("name")
        address = data.get("address")
        phone = data.get("phone")
        cuisine_type = data.get("cuisine_type")  # 注意：前端是 cuisine_type
        price_range = data.get("price_range")
        rating = data.get("rating")
        description = data.get("description")

        if not name or not address:
            return jsonify({"status": False, "message": "name和address不能为空"})

        if rating:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 5:
                return jsonify({"status": False, "message": "评分必须在 0-5 之间"})

        if price_range:
            if float(price_range) < 0:
                return jsonify({"status": False, "message": "价格不能为负数"})

        insert(
            "INSERT INTO restaurants (name, address, phone, cuisine_type, price_range, rating, description) VALUES(%s,%s,%s,%s,%s,%s,%s)",
            [name, address, phone, cuisine_type, price_range, rating, description])

        return jsonify({"status": True, "message": "添加成功"})


@restaurants.route("/api/search", methods=["POST"])
def search():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": False, "message": "请求数据为空"})

        name = data.get("name", "").strip()
        cuisine_type = data.get("cuisine_type", "").strip()
        price_range = data.get("price_range", "").strip()

        # 构建查询条件和参数
        conditions = []
        params = []

        if name:
            conditions.append("name LIKE %s")
            params.append(f"%{name}%")

        if cuisine_type:
            conditions.append("cuisine_type = %s")  # 使用等号进行精确匹配
            params.append(cuisine_type)

        if price_range:
            if price_range == "￥":
                conditions.append("price_range < %s")
                params.append(50)
            elif price_range == "￥￥":
                conditions.append("price_range BETWEEN %s AND %s")
                params.extend([50, 100])
            elif price_range == "￥￥￥":
                conditions.append("price_range > %s")
                params.append(100)
        # 如果没有查询条件
        if not conditions:
            return jsonify({
                "status": False,
                "message": "请至少输入一个查询条件"
            })

        # 构建完整查询
        where_clause = " AND ".join(conditions)
        full_query = f"SELECT * FROM restaurants WHERE {where_clause}"

        print(f"执行查询: {full_query}")
        print(f"参数: {params}")

        data_list = search_sql(full_query, params)

        if data_list:
            return jsonify({
                "status": True,
                "message": data_list,
                "count": len(data_list)
            })
        else:
            return jsonify({
                "status": False,
                "message": f"暂无符合条件的餐馆信息"
            })

    except Exception as e:
        print(f"搜索错误: {str(e)}")
        return jsonify({"status": False, "message": f"搜索失败: {str(e)}"})


# ai客服
@ai.route("/api/ai/chat", methods=["POST"])
def ai_chat():
    try:
        data = request.get_json()
        print(f"接收到的数据: {data}")  # 调试日志

        content = data.get('content', '')
        print(f"消息内容: {content}")  # 调试日志

        data_list = fetch_all("select * from restaurants")
        print(f"获取到 {len(data_list)} 家餐馆")  # 调试日志

        if not content:
            return jsonify({"error": "内容不能为空"}), 400

        # 构建餐馆数据系统提示
        restaurants_data = ""
        for restaurant in data_list:
            restaurants_data += f"""
名称：{restaurant.get('name', '')}
类型：{restaurant.get('type', '')}
人均价格：{restaurant.get('price', '')}元
评分：{restaurant.get('rating', '')}
地址：{restaurant.get('address', '')}
特色菜：{restaurant.get('specialty', '')}
描述：{restaurant.get('description', '')}
---
"""

        system_prompt = f"""你是一个长沙餐馆推荐助手。请根据用户的需求，从以下餐馆数据库中推荐合适的餐馆。

餐馆数据库：
{restaurants_data}

推荐规则：
1. 根据用户的价格偏好、菜系类型、地理位置等需求进行推荐
2. 每次推荐1-3家最符合要求的餐馆
3. 提供详细的推荐理由，包括价格、特色、评分等信息
4. 如果用户需求不明确，可以询问具体偏好
5. 回复要友好、专业，突出每家餐馆的特色

请基于以上信息为用户提供餐馆推荐："""

        # 构建消息列表，加入系统提示
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # 添加历史对话记录
        if isinstance(content, list):
            messages.extend(content)
        else:
            messages.append({"role": "user", "content": content})

        print(f"发送给AI的消息: {messages}")  # 调试日志

        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        completion = client.chat.completions.create(
            model="qwen3-max",
            messages=messages,
            stream=True
        )

        # 收集AI回复
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content

        # 保存到数据库
        if isinstance(content, list) and content:
            user_content = content[-1].get("content", "")
        else:
            user_content = content

        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        print(f"用户问题: {user_content}")
        print(f"AI回答: {full_response}")

        # 插入数据库（添加错误处理）
        try:
            insert("INSERT INTO question_table (question, messages, time) VALUES (%s,%s,%s)",
                   [user_content, full_response, times])
        except Exception as db_error:
            print(f"数据库插入错误: {db_error}")

        return jsonify({"response": full_response})

    except Exception as e:
        print(f"AI聊天接口错误: {str(e)}")
        print(f"错误类型: {type(e)}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


@ai.route("/api/ai/List", methods=["GET"])
def aiList():
    if request.method == "GET":
        data_list = fetch_all("select * from question_table")
        print(data_list)

        if data_list:
            # 确保返回的是列表格式
            return jsonify({"status": True, "message": data_list})
        else:
            # 返回空数组而不是字符串
            return jsonify({"status": True, "message": []})
