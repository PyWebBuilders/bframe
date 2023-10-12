# 创建用户
curl http://localhost:7256/users -X POST -d "username=tom&password=tom"
# 创建问题
curl http://localhost:7256/questions -X POST -d "content=你喜欢下雨天气么？"
# 获取问题
curl http://localhost:7256/questions
# 创建问题答案
curl http://localhost:7256/choices -X POST -d "question=1&content=喜欢"
curl http://localhost:7256/choices -X POST -d "question=1&content=不喜欢"
# 获取问题答案
curl http://localhost:7256/choices
# 创建投票
curl http://localhost:7256/user_choices -X POST -d "userid=1&choiceid=1"
# 查询投票
curl http://localhost:7256/user_choices