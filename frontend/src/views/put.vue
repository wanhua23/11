<template>
    <div class="order-detail">
      <el-card class="box-card" style="max-width: 480px">
        <template #header>
          <div class="card-header">
            <span>更新餐馆</span>
          </div>
        </template>
        
        <el-form
          ref="formRef"
          label-position="left"
          label-width="auto"
          :model="formLabelAlign"
          :rules="rules"
          style="max-width: 600px; width: 100%;"
        >
          <el-form-item label="餐馆名称" prop="name">
            <el-input v-model="formLabelAlign.name" />
          </el-form-item>
          <el-form-item label="详细地址" prop="address">
            <el-input v-model="formLabelAlign.address" />
          </el-form-item>
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="formLabelAlign.phone" />
          </el-form-item>
          <el-form-item label="菜系类型" prop="cuisine_type">
            <el-select 
              v-model="formLabelAlign.cuisine_type" 
              placeholder="请选择菜系类型"
              style="width: 100%"
              clearable
              filterable
              allow-create
            >
              <el-option
                v-for="cuisine in cuisineOptions"
                :key="cuisine.value"
                :label="cuisine.label"
                :value="cuisine.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="价格区间" prop="price_range">
            <el-input v-model="formLabelAlign.price_range" />
          </el-form-item>
          <el-form-item label="评分(0-5分)" prop="rating">
            <el-input v-model="formLabelAlign.rating" type="number" min="0" max="5" step="0.1" />
          </el-form-item>
          <el-form-item label="餐馆描述" prop="description">
            <el-input v-model="formLabelAlign.description" type="textarea" :rows="3" />
          </el-form-item>
        </el-form>
        
        <el-button type="primary" style="margin-top: 20px;" @click="submitForm">提交</el-button>
        
      </el-card>
    </div>
  </template>
  
  <script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from "axios"
import { Plus } from '@element-plus/icons-vue'


const route = useRoute()
const router = useRouter()
const formRef = ref()
const currentId = ref('')

const formLabelAlign = reactive({
  name: '',
  address: '',
  phone: '',
  cuisine_type: '',
  price_range: '',
  rating: '',
  description: '',
  image_url: '' 
})

const cuisineOptions = ref([
  { label: '川菜', value: '川菜' },
  { label: '湘菜', value: '湘菜' },
  { label: '粤菜', value: '粤菜' },
  { label: '鲁菜', value: '鲁菜' },

])

  
const rules = {
    name: [
      { required: true, message: '请输入餐馆名称', trigger: 'blur' }
    ],
    address: [
      { required: true, message: '请输入详细地址', trigger: 'blur' }
    ],
    price_range: [
    { 
      validator: (rule, value, callback) => {
        if (value && parseFloat(value) < 0) {
          callback(new Error('价格不能为负数'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  rating: [
    {
      validator: (rule, value, callback) => {
        if (!value) {
          callback() // 允许为空
          return
        }
        const num = parseFloat(value)
        if (isNaN(num)) {
          callback(new Error('请输入数字'))
        } else if (num < 0 || num > 5) {
          callback(new Error('评分必须在0-5之间'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  }

// 获取餐馆数据
async function getRestaurantData(id) {
  try {
    console.log('正在获取ID为:', id, '的餐馆数据')
    const res = await axios({
      url: `http://127.0.0.1:5000/api/restaurants/${id}`,
      method: "get"
    })
    // 判断后端状态码是否返回正常
    if (res.data.status) {
      // 将获取的数据填充到表单中
      Object.assign(formLabelAlign, res.data.message)
      console.log('获取到的餐馆数据:', res.data.message)
    } else {
      ElMessage.error('获取餐馆数据失败: ' + res.data.message)
    }
  } catch (error) {
    console.error('获取餐馆数据时出错:', error)
    ElMessage.error('获取餐馆数据失败')
  }
}

// 提交表单
async function submitForm() {
  if (!formRef.value) return
      // 更新现有餐馆
      const res = await axios({
        url: `http://127.0.0.1:5000/api/restaurants/${currentId.value}`,
        method: "PUT",
        data: formLabelAlign
      })
      
      if (res.data.status) {
        ElMessage.success('更新成功！')
        goBack()
      } else {
        ElMessage.error('更新失败: ' + res.data.message)
      }
    }
// 返回上一页
function goBack() {
  router.back()
}
// 页面加载时获取ID并加载数据
onMounted(() => {
  console.log('路由参数:', route.query)
  
  // 从query参数获取ID
  currentId.value = route.query.id
  getRestaurantData(currentId.value)
})



  </script>
  
  <style scoped>
  .order-detail {
    padding: 20px;
    background-color: #f5f7fa;
    min-height: 50vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;

  }
  
  .box-card {
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }
  
  .card-header {
    font-size: 18px;
    font-weight: bold;
    text-align: center;
  }
  </style>