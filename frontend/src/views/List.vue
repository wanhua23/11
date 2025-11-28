<template>
    <el-container style="display: flex; flex-direction: column; padding-left: 20px; height: 100vh;">
        <!-- 搜索区域 -->
        <div style="margin-top: 16px; margin-bottom: 16px;">
            <el-input v-model="searchForm.name" style="width: 240px" placeholder="输入查询的餐馆名" />
            <el-select 
              v-model="searchForm.cuisine_type" 
              placeholder="请选择菜系类型"
              style="width: 100px"
            >
              <el-option
                v-for="cuisine in cuisineOptions"
                :key="cuisine.value"
                :label="cuisine.label"
                :value="cuisine.value"
              />
            </el-select>
            <el-select 
              v-model="searchForm.price_range" 
              placeholder="请选择价格区间"
              style="width: 100px"
            >
              <el-option
                v-for="cuisine in priceOptions"
                :key="cuisine.value"
                :label="cuisine.label"
                :value="cuisine.value"
              />
            </el-select>
            <el-button 
                :icon="Search" 
                circle 
                @click="search()"
                />
        </div>
        
        <div style="height: auto; overflow: hidden;">
        <el-table 
            :data="currentPageData" 
            style="width: 100%"
            :max-height="550"
            :header-cell-style="{ background: '#f5f7fa' }"
        >
            <el-table-column prop="name" label="餐馆名称" width="150" />
            <el-table-column prop="address" label="详细地址" width="600" />
            <el-table-column prop="cuisine_type" label="菜系类型" width="120" />
            <el-table-column prop="price_range" label="价格" width="120" />
            <el-table-column prop="rating" label="评分" width="120" />
            <el-table-column fixed="right" label="操作" min-width="120">
                <template #default="scope">
                    <el-button 
                        type="primary" 
                        :icon="Edit" 
                        circle 
                        @click="one(scope.row.id)"
                        />
                    <el-button 
                        type="danger" 
                        :icon="Delete" 
                        circle 
                        @click="del(scope.row.id)"
                    />
                </template>
            </el-table-column>
        </el-table>
    </div>

        <!-- 分页组件 - 固定在底部 -->
        <div style="bottom: 200px; background: white; padding: 16px 0; border-top: 1px solid #e4e7ed; z-index: 100;">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              background
              layout="total, prev, pager, next, jumper"
              :total="restaurants.length"
              class="mt-4"
              style="justify-content: center;"
            />
        </div>
    </el-container>
</template>


<script setup>
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router' 
import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'
import axios from "axios"
import { ref,reactive, computed } from 'vue'

    const router = useRouter()
    const restaurants = ref([]);  
    const searchForm = reactive({
      name: '',
      cuisine_type: '',
      price_range: ''
      })
    const cuisineOptions = ref([
  { label: '川菜', value: '川菜' },
  { label: '湘菜', value: '湘菜' },
  { label: '粤菜', value: '粤菜' },
  { label: '鲁菜', value: '鲁菜' },
])
const priceOptions = ref([
  { label: '50以下', value: '￥' },
  { label: '50-100', value: '￥￥' },
  { label: '100以上', value: '￥￥￥' }
])

    async function getData(){
      const res = await axios({
        url: "http://127.0.0.1:5000/api/restaurants",
        method: "get",
      })
      restaurants.value = res.data.message
      console.log(res.data.message)
    }
    getData()


    async function search(){
      const res = await axios({
        url: "http://127.0.0.1:5000/api/search",
        method: "post",
        data:{
          name: searchForm.name.trim(),
          cuisine_type: searchForm.cuisine_type,
          price_range:searchForm.price_range
      }
      })
      if (res.data.status) {
        restaurants.value = res.data.message
        currentPage.value = 1 // 重置到第一页
        ElMessage.success('搜索成功！')
      } else {
        ElMessage.error('搜索失败！'+ res.data.message)
      }
      }
  

    const currentPage = ref(1)  // 当前页码
    const pageSize = ref(10)    // 每页显示条数

    const currentPageData = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return restaurants.value.slice(start, end)
})
    


    async function del(id){
      if (!confirm('确定要删除这条记录吗？')) {
          return;
      }
      const res = await axios({
        url: `http://127.0.0.1:5000/api/restaurants/${id}`,
        method: "DELETE"
      })
      if (res.data.status) {
            ElMessage.success('删除成功！')
            getData()
        } else {
            alert("删除失败: " + res.data.message);
        }
    }

  async function one(id){
  console.log("编辑ID:", id)
  
  // 直接跳转到编辑页面，并传递ID作为参数
  router.push({
    path: '/manager/put',
    query: {
      id: id
    }
  })
  
}

</script>
<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
.layout-container-demo .el-header {
  position: relative;
  background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary);
}
.layout-container-demo .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
}
.layout-container-demo .el-menu {
  border-right: none;
}
.layout-container-demo .el-main {
  padding: 0;
}
.layout-container-demo .toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}
</style>