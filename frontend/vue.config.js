module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  devServer: {
    proxy: {
      '/api*': {
        // Forward frontend dev server request for /api to flask dev server
        target: 'http://localhost:5000/',
        changeOrigin: true
      },
      '/user*': {
        // Forward frontend dev server request for /user to flask dev server
        target: 'http://localhost:5000/',
        changeOrigin: true
      },
    }
  }
}