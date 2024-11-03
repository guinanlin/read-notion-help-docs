from fastapi.testclient import TestClient
from app.main import app
from app.utils.security import get_password_hash

client = TestClient(app)

# def test_read_users_me(client, test_user):
#     # 首先登录获取token
#     login_response = client.post(
#         "/token",
#         data={
#             "username": "tim",
#             "password": "secret123"
#         }
#     )
#     access_token = login_response.json()["access_token"]
    
#     # 使用token访问用户信息
#     headers = {"Authorization": f"Bearer {access_token}"}
#     response = client.get("/users/me/", headers=headers)
#     assert response.status_code == 200
#     user_data = response.json()
#     assert user_data["username"] == "guinan"
#     assert user_data["email"] == "goodhawk@gmail.com" 

# def test_get_password_hash():
#     password = "123456"
#     hashed_password = get_password_hash(password)
#     assert hashed_password is not None
#     assert hashed_password != password
#     # 验证哈希密码是否正确
#     assert verify_password(password, hashed_password)

# pytest -s tests/test_user.py
def test_get_password_hash():
    password = "123456"  # 替换为你想要哈希的密码
    hashed_password = get_password_hash(password)
    print(f"Hashed password: {hashed_password}")  # 输出哈希密码
    assert hashed_password is not None
    assert hashed_password != password
    print(f"Hashed password: {hashed_password}")  # 输出哈希密码