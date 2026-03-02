/**
 * 后端 API 封装
 * 请将 BASE_URL 改为实际部署的后端地址
 */
const BASE_URL = 'http://localhost:8000'

function request(method, url, data = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      method,
      data,
      header: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          reject(new Error(res.data?.detail || '请求失败'))
        }
      },
      fail: (err) => reject(err)
    })
  })
}

/**
 * 上传图片
 * @param {string} filePath - 本地临时文件路径（uni.chooseImage 返回）
 */
export function uploadImage(filePath) {
  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: BASE_URL + '/api/upload/image',
      filePath,
      name: 'file',
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            const data = JSON.parse(res.data)
            resolve(data.url)
          } catch (e) {
            reject(new Error('解析响应失败'))
          }
        } else {
          reject(new Error(res.data || '上传失败'))
        }
      },
      fail: reject
    })
  })
}

/**
 * 创建试衣任务
 * @param {string} personImageUrl - 模特图 URL（oss:// 或 https://）
 * @param {string} garmentImageUrl - 服饰图 URL
 */
export function createTryon(personImageUrl, garmentImageUrl) {
  return request('POST', '/api/tryon/create', {
    person_image_url: personImageUrl,
    garment_image_url: garmentImageUrl
  })
}

/**
 * 查询试衣结果
 * @param {string} taskId - 任务 ID
 */
export function getTryonResult(taskId) {
  return request('GET', '/api/tryon/result', { task_id: taskId })
}
