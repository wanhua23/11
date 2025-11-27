<template>
  <div class="chat-container">
    <!-- 聊天头部 -->
    <div class="chat-header">
      <h3>🍽️ 长沙餐馆助手</h3>
      <div style="display: flex; align-items: center; gap: 8px;">
        <el-button 
          type="text" 
          @click="clearHistory"
          :disabled="messages.length === 0"
        >
          清空记录
        </el-button>
        <el-button 
          type="text" 
          @click="history"
        >
          历史记录
        </el-button>
      </div>
    </div>

    <!-- 消息区域 -->
    <div class="messages-container" ref="messagesContainer">
      <div 
        v-for="(message, index) in messages" 
        :key="index" 
        :class="['message', message.role]"
      >
        <!-- AI消息 -->
        <div v-if="message.role === 'assistant'" class="message-left">
          <div class="avatar">AI</div>
          <div class="message-content">
            <div class="message-bubble assistant-bubble">
              {{ message.content }}
              <div class="message-time">{{ message.time }}</div>
            </div>
          </div>
        </div>

        <!-- 用户消息 -->
        <div v-else class="message-right">
          <div class="message-content">
            <div class="message-bubble user-bubble">
              {{ message.content }}
              <div class="message-time">{{ message.time }}</div>
            </div>
          </div>
          <div class="avatar">我</div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="message-left">
        <div class="avatar">AI</div>
        <div class="message-content">
          <div class="message-bubble assistant-bubble">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-container">
      <div class="input-wrapper">
        <el-input
          v-model="userInput"
          type="textarea"
          :rows="2"
          placeholder="请输入您的问题，例如：推荐一家价格适中的湘菜馆..."
          @keydown.enter.exact.prevent="sendMessage"
        />
        <el-button 
          type="primary" 
          @click="sendMessage"
          :disabled="!userInput.trim() || loading"
          class="send-btn"
          :loading="loading"
        >
          {{ loading ? '思考中...' : '发送' }}
        </el-button>
      </div>
      
      <!-- 快捷问题 -->
      <div class="quick-questions">
        <span class="quick-title">快捷提问：</span>
        <el-button 
          v-for="(question, index) in quickQuestions" 
          :key="index"
          size="small"
          @click="handleQuickQuestion(question)"
          :disabled="loading"
        >
          {{ question }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

// 响应式数据
const userInput = ref('')
const loading = ref(false)
const messagesContainer = ref(null)
const restaurants = ref([]); 

// 消息列表
const messages = reactive([])

// 快捷问题示例
const quickQuestions = [
  '推荐一家价格适中的湘菜馆',
  '长沙有哪些必吃的本地菜？',
  '五一广场附近有什么好吃的？',
  '人均100元左右的餐厅推荐'
]

// 发送消息
const sendMessage = async () => {
  const content = userInput.value.trim()
  if (!content) return
  
  // 添加用户消息
  const userMessage = {
    role: 'user',
    content: content,
    time: new Date().toLocaleTimeString()
  }
  messages.push(userMessage)
  scrollToBottom()
  
  // 清空输入框
  userInput.value = ''
  
  // 设置加载状态
  loading.value = true
  
  try {
    // 发送请求到后端
    const res = await axios({
      url: `http://127.0.0.1:5000/api/ai/chat`,
      method: "POST",
      data: {
        content: messages
      }
    })
    
    console.log('响应数据:', messages)
    
    // 添加AI回复消息
    const aiMessage = {
      role: 'assistant',
      content: res.data.response || res.data,
      time: new Date().toLocaleTimeString()
    }
    messages.push(aiMessage)
    
    ElMessage.success('回复完成')
    scrollToBottom()
    
  } catch (error) {
    console.error('请求错误:', error)
    
    // 添加错误消息
    const errorMessage = {
      role: 'assistant',
      content: '抱歉，我暂时无法回复您的问题。请稍后重试。',
      time: new Date().toLocaleTimeString()
    }
    messages.push(errorMessage)
    
    ElMessage.error(error.response?.data?.error || '请求失败')
  } finally {
    loading.value = false
    // 滚动到底部
    scrollToBottom()
  }
}

// 处理快捷问题
const handleQuickQuestion = (question) => {
  userInput.value = question
  // 稍等一下让输入框更新，然后发送
  nextTick(() => {
    sendMessage()
  })
}

// 清空对话历史
const clearHistory = () => {
  messages.length = 0
  // 重新添加欢迎消息
  const welcomeMessage = {
    role: 'assistant',
    content: `您好！我是长沙餐馆助手，可以为您推荐餐厅、解答相关问题。请问有什么可以帮助您的？${restaurants.value}`,
    time: new Date().toLocaleTimeString()
  }
  messages.push(welcomeMessage)
  ElMessage.success('对话记录已清空')
}

const history = () =>{
  router.push({
    path: '/manager/ailist'
  })
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

async function getData(){
  const res = await axios({
    url: "http://127.0.0.1:5000/api/restaurants",
    method: "get",
  })
  restaurants.value = res.data.message
  
  const welcomeMessage = {
    role: 'assistant',
    content: `您好！我是长沙餐馆助手，已为您加载 ${restaurants.value.length} 家优质餐厅。我可以为您推荐餐厅、查询特色菜品或根据偏好筛选。请问您想了解什么？`,restaurants,
    time: new Date().toLocaleTimeString()
  }
  messages.push(welcomeMessage)
  console.log("餐馆数据：",restaurants.value)
}

onMounted(() => {
  getData()
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 700px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  background: #fff;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e4e7ed;
  background: #f5f7fa;
}

.chat-header h3 {
  margin: 0;
  color: #303133;
}

.messages-container {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #fafafa;
}

.message {
  margin-bottom: 20px;
}

.message-left, .message-right {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
}

.message-right {
  justify-content: flex-end;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  color: white;
  flex-shrink: 0;
}

.message-left .avatar {
  background: #409eff;
  margin-right: 12px;
}

.message-right .avatar {
  background: #67c23a;
  margin-left: 12px;
  order: 2;
}

.message-content {
  max-width: 70%;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 8px;
  position: relative;
  word-wrap: break-word;
}

.assistant-bubble {
  background: white;
  border: 1px solid #e4e7ed;
  color: #606266;
}

.user-bubble {
  background: #409eff;
  color: white;
}

.message-time {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 4px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  height: 20px;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background: #c0c4cc;
  border-radius: 50%;
  display: inline-block;
  margin: 0 2px;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.input-container {
  border-top: 1px solid #e4e7ed;
  padding: 16px 20px;
  background: #fff;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.input-wrapper :deep(.el-textarea) {
  flex: 1;
}

.send-btn {
  align-self: flex-end;
  height: auto;
  min-height: 56px;
}

.quick-questions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-title {
  font-size: 12px;
  color: #909399;
  margin-right: 8px;
}

.quick-questions .el-button {
  font-size: 12px;
}
</style>