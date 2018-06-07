# 项目名称：图书馆管理系统

## 预计功能

- Administrator：

  - 添加、减少书籍
  - 查询书籍储存情况
  - 修改书籍信息
  - 修改个人信息
  - ~~创建、删除Normal~~

- Normal：

  - 查询书籍
  - 借阅书籍，归还书籍
  - 续借书籍
  - 修改个人信息

## 使用语言及框架

- 前端
  - HTML、CSS、JS
  - jQuery、bootstrap
- 后端
  - Python
  - Flask、Jinja2

## 数据库

#### 使用

- SQLite

#### 设计

- Book
- Normal
- Admin
- Borrow

## 预计页面

- 首页、直接登陆（分普通用户、管理员用户）
- 账户管理界面
- 图书浏览界面
- 借阅、归还页面

## API

### User API

- Login(all)

  ```
  请求地址：/api/user/login
  请求方式：POST
  请求格式：json
  请求参数：
  {
  	email,
  	password,
  	remember
  }
  响应参数：
  status: {
  	'200': 'success and User',
  	'201': 'success and Admin',
  	'202': 'accont dosen't exist',
  	'203': 'wrong password',
  	'400': 'other'
  }
  ```

- Logout(all)

  ```
  请求地址：/api/user/logout
  请求方式：GET
  ```

  ​

- Register(only user)

  ```
  请求地址：/api/user/register
  请求方式：POST
  请求格式：json
  请求参数：
  {
  	email,
  	password,
  	username
  }
  响应参数：
  status: {
  	'200': 'success',
  	'201': 'account has existed',
  	'400': 'other'
  }
  ```

- Modify(all)

  ```
  请求地址：/api/user/modify
  请求方式：POST
  请求格式：json
  请求参数：
  {
  	new_email(optional),
  	new_password(optional),
  	new_username(optional),
  }
  响应参数：
  status: {
  	'200': 'success',
  	'201': 'failed',
  	'400': 'other'
  }
  ```

### Admin API

见User API

包含`Login` `Logout` `Modify` 

请求地址中所有`user`改为`admin`

- search

  ```
  请求地址：/api/admin/search
  请求方式：POST
  请求格式：json
  请求参数：username、user-id、email(at least one)
  响应参数：
  status: {
  	'200': 'success',
  	user-list: {
  		id,
  		username,
  		email
  	}
  	'201': 'not found',
  	'202': 'other'
  }
  ```

### BOOK API

- Search(all)

  ```
  请求地址：/api/book/search
  请求方式：POST
  请求格式：json
  请求参数：id、name、author(at least one)
  响应格式：json
  响应参数：
  status: {
  	'200': 'success',
  		book-list: {
  			id,
  			name,
  			available,
  			number(only for admin),
  			summary(only for admin),
  			max_time,
  			author
  		}
  	'201': 'not found',
  	'400': 'other'
  }
  ```

- Borrow(only user)

  ```
  请求地址：/api/book/borrow
  请求方式：POST
  请求格式：json
  请求参数：id
  响应参数：
  status: {
  	'200': 'success',
  	'201': 'failed',
  	'400': 'other'
  }
  ```

- Return(only user)

  ```
  请求地址：/api/book/return
  请求方式：POST
  请求格式：json
  请求参数：id
  响应参数：
  status: {
  	'200': 'success',
  	'201': 'failed',
  	'400': 'other'
  }
  ```

- Add(admin, root)

  ```
  请求地址：/api/book/add
  请求方式：POST
  请求格式：json
  请求参数：
  {
  	id(optional)
  	name,
  	number(default=1),
  	max_time(default=30),
  	author
  }
  响应参数：
  status: {
  	'200': 'success',
  	'201': 'failed',
  	'400': 'other'
  }
  ```

- Remove(admin, root)

  ```
  请求地址：/api/book/remove
  请求方式：POST
  请求格式：json
  请求参数：
  {
  	id,
  	number(default=1)
  }
  响应参数：
  status: {
  	'200': 'success',
  	'201': 'failed',
  	'400': 'other'
  }
  ```

- Modify(admin, root)

  ```
  请求地址：/api/book/modify
  请求方式：POST
  请求格式：json
  请求参数：
  {
  	id,
  	summary(optional),
  	max_time(optional),
  	author(optional)
  }
  响应参数：
  status: {
  	'200': 'success',
  	'201': 'failed',
  	'400': 'other'
  }
  ```
