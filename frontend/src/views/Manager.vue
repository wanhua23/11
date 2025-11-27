<template>
        <el-container>
           <!-- 左边 -->
    <el-row class="tac">
      <el-col :span="12">
        <el-menu
          router
          :default-active="router.currentRoute.value.path"
          class="el-menu-vertical-demo"
          style="border-right: 1px solid #e4e7ed; "
          :text-color="'#303133'"        
          :active-text-color="'#409EFF'" 
        >
          <el-menu-item index="/manager/list" style="border-bottom: 1px solid #e4e7ed;">
            <span>餐馆列表</span>
          </el-menu-item>
          <el-menu-item index="/manager/ai" style="border-bottom: 1px solid #e4e7ed;">
            <span>AI客服</span>
          </el-menu-item>
          <el-menu-item index="/manager/add">
            <span>添加餐馆</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
      <!-- 右边 -->
      <router-view></router-view>
        </el-container>
  </template>
<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
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