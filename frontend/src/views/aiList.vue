<template>

    <div class="table-container">
        <div class="button-example">
    <div class="button-row">
      <el-button type="primary"
                 @click="back()"
                >返回</el-button>
    </div>
    </div>
        <el-table 
            :data="currentPageData" 
            style="width: 100%; height: 100%"
            :max-height="tableHeight"
            :header-cell-style="{ background: '#f5f7fa', fontWeight: 'bold' }"
            :cell-style="{ padding: '8px' }"
        >
            <el-table-column 
                prop="question" 
                label="用户发出信息" 
                width="200"
                show-overflow-tooltip
            />
            <el-table-column 
                prop="messages" 
                label="AI回答" 
                min-width="400"
                show-overflow-tooltip
            />
            <el-table-column 
                prop="time" 
                label="时间" 
                width="150"
            />
        </el-table>
        
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
    </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router' 
import axios from "axios"
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'

const restaurants = ref([])
const tableHeight = ref(500)
const router = useRouter()

const back = () =>{
    router.push({
        path: "/manager/ai"
})
}

// 计算表格高度
const calculateTableHeight = () => {
    const windowHeight = window.innerHeight
    const headerHeight = 60 // 预估头部高度
    const paginationHeight = 60 // 分页组件高度
    const margin = 40 // 边距
    
    tableHeight.value = windowHeight - headerHeight - paginationHeight - margin
}

async function getData(){
    try {
        const res = await axios({
            url: "http://127.0.0.1:5000/api/ai/List",
            method: "get",
        })
        restaurants.value = res.data.message || []
        ElMessage.success('数据加载成功')
    } catch (error) {
        console.error('获取数据失败:', error)
        ElMessage.error('数据加载失败')
        restaurants.value = []
    }
}

const currentPage = ref(1)
const pageSize = ref(10)

const currentPageData = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return restaurants.value.slice(start, end)
})

// 监听窗口大小变化
onMounted(() => {
    getData()
    calculateTableHeight()
    window.addEventListener('resize', calculateTableHeight)
})

onUnmounted(() => {
    window.removeEventListener('resize', calculateTableHeight)
})
</script>

<style scoped>
.table-container {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    padding: 20px;
    box-sizing: border-box;
    background: #f5f7fa;
}

:deep(.el-table) {
    flex: 1;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

:deep(.el-table .el-table__body-wrapper) {
    overflow-y: auto;
}

:deep(.el-table th) {
    color: #303133;
    font-size: 14px;
}

:deep(.el-table td) {
    color: #606266;
    font-size: 13px;
}

.pagination-container {
    margin-top: 16px;
    padding: 16px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: flex-end;
}

:deep(.el-pagination) {
    padding: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .table-container {
        padding: 10px;
    }
    
    :deep(.el-table .el-table__cell) {
        padding: 4px 0;
    }
}

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