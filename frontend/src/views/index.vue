<template>
    <VChart class="chart-container" :option="pieOption" />
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import VChart from "vue-echarts";
import axios from 'axios';

// 响应式数据
const pieOption = reactive({
  title: {
    text: '菜品类型分布',
    left: 'center'
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '菜品类型',
      type: 'pie',
      radius: '50%',
      data: [], // 初始为空，从API获取数据后填充
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
})

// 获取数据并更新图表
const fetchRestaurantData = async () => {
  try {
    const res = await axios({
      url: "http://127.0.0.1:5000/api/restaurants",
      method: "get",
    })
    
    console.log('API响应数据:', res.data)
    
    if (res.data.status && res.data.message) {
      // 处理数据：统计每种菜品类型的数量
      const typeCount = {}
      
      res.data.message.forEach(restaurant => {
        const cuisineType = restaurant.cuisine_type || '未知类型'
        typeCount[cuisineType] = (typeCount[cuisineType] || 0) + 1
      })
      
      console.log('菜品类型统计:', typeCount)
      
      // 转换为ECharts需要的格式
      const chartData = Object.keys(typeCount).map(type => ({
        value: typeCount[type],
        name: type
      }))
      
      console.log('图表数据:', chartData)
      
      // 更新图表数据
      pieOption.series[0].data = chartData
    } else {
      console.warn('API返回数据格式异常')
    }
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchRestaurantData()
})
</script>

<style scoped>
.chart-container {
  height: 400px;
  width: 100%;
}
</style>