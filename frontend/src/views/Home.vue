<template>
  <div class="home">
    <div class="hero">
      <h1>Welcome to MeetingHub</h1>
      <p>高效会议，轻松管理</p>
      <div class="actions">
        <el-button type="primary" size="large" @click="$router.push('/login')">登录</el-button>
        <el-button size="large" @click="$router.push('/login#reg')">注册</el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}
.hero {
  text-align: center;
}
.hero h1 {
  font-size: 48px;
  margin-bottom: 16px;
}
.hero p {
  font-size: 20px;
  margin-bottom: 32px;
}
.actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}
</style>