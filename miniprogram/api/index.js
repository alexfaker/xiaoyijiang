/**
 * 后端 API 封装
 * 体验版/正式版必须：1) 使用 HTTPS  2) 使用已备案域名  3) 在微信公众平台配置 request 合法域名
 */
const BASE_URL = 'https://drama.flashwave.cn/xiaoyijiang'  // 通过 Nginx 转发到 8000 端口

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
            if (data.diagnostic === 'GET_not_allowed') {
              reject(new Error('上传请求被错误发成 GET，请检查网络/域名配置，或使用 HTTPS'))
              return
            }
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
