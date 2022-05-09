function Alert() {
  this.install = (Vue) => {
    Vue.prototype.$alert = this;
  }
  this.onAlert = () => {};
  this.showAlert = (message) => {
    this.onAlert(message);
  }
}

export default new Alert();

