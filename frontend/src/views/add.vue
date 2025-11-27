<template>
  <div style="display: flex; flex-direction: column; padding-top: 20px; padding-left: 500px;">
    
    <el-form
      label-position="left"
      label-width="auto"
      :model="formLabelAlign"
      :rules="rules"
      ref="formRef"
      style="max-width: 600px; width: 100%;"
    >
      <!-- 其他表单项保持不变 -->
      <el-form-item label="餐馆名称" prop="name" >
        <el-input v-model="formLabelAlign.name"  />
      </el-form-item>
      <el-form-item label="详细地址" prop="address">
        <el-input v-model="formLabelAlign.address"  />
      </el-form-item>
      <el-form-item label="联系电话" prop="phone">
        <el-input v-model="formLabelAlign.phone"  />
      </el-form-item>
      <el-form-item label="菜系类型" prop="cuisine_type">
          <el-select 
          v-model="formLabelAlign.cuisine_type" 
          placeholder="请选择菜系类型"
          style="width: 100%"
        >
          <el-option
            v-for="cuisine in cuisineOptions"
            :label="cuisine.label"
            :value="cuisine.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="价格区间" prop="price_range">
        <el-input v-model="formLabelAlign.price_range"  />
      </el-form-item>
      <el-form-item label="评分(0-5分)" prop="rating">
        <el-input v-model="formLabelAlign.rating" type="number" min="0" max="5" step="0.1" />
      </el-form-item>
      <el-form-item label="餐馆描述" prop="description">
        <el-input v-model="formLabelAlign.description" type="textarea" :rows="3" />
      </el-form-item>
    </el-form>
    <el-button type="primary" style="margin-top: 20px;" @click="addData()">提交</el-button>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// 表单数据
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


// 其他代码保持不变
const cuisineOptions = ref([
  { label: '川菜', value: '川菜' },
  { label: '湘菜', value: '湘菜' },
  { label: '粤菜', value: '粤菜' },
  { label: '鲁菜', value: '鲁菜' }
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

const formRef = ref()

async function addData() {
  try {
    await formRef.value.validate()
    
    const response = await axios({
      url: "http://127.0.0.1:5000/api/restaurants",
      method: "post",
      data: {
        name: formLabelAlign.name,
        address: formLabelAlign.address,
        phone: formLabelAlign.phone,
        cuisine_type: formLabelAlign.cuisine_type,
        price_range: formLabelAlign.price_range,
        rating: formLabelAlign.rating,
        description: formLabelAlign.description,
        image_url: formLabelAlign.image_url // 添加图片URL
      }
    })
    
    if (response.data.status) {
      ElMessage.success('添加成功！')
      // 重置表单
      formRef.value.resetFields()
      // 同时重置图片URL
      formLabelAlign.image_url = ''
    } else {
      ElMessage.error('添加失败: ' + response.data.message)
    }
  } catch (error) {
    ElMessage.error('提交失败: ' + error.message)
  }
}
</script>

<style scoped>
/* 样式保持不变 */
.button-example {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

.button-row > * {
  margin: 0;
}

.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
  object-fit: cover;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 7px;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
  line-height: 178px;
}
</style>