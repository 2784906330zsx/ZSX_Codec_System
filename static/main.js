function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

const app = new Vue({
    el: "#app",
    data: {
        inputText1: "",
        inputText2: "",
        inputText3: "",
    },
    methods: {
        handleInput1: debounce(function (event) {
            if (this.inputText1 === "DWC") {
                window.location.href = 'https://love.sdju.chat';
            } else if (this.inputText1 === "蔡鑫培Peter") {
                window.location.href = 'https://space.bilibili.com/123016785/favlist';
            } else {
                this.lock();
            }
        }, 500),

        handleInput2: debounce(function (event) {
            if (event.isTrusted) {
                this.unlock();
            }
        }, 500),

        copyToClipboard(text) {
            if (text) {
                navigator.clipboard.writeText(text).then(() => {
                }).catch(err => {
                    console.error("无法复制内容：", err);
                });
            }
        },

        lock() {
            fetch("/lock", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: this.inputText1,
                }),
            })
                .then((response) => {
                    console.log(response);
                    if (response.redirected) {
                        window.location.href = response.url;
                        return { response: '' };
                    }

                    return response.json();
                })
                .then((data) => {
                    this.inputText2 = data.response;
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
        },

        unlock() {
            fetch("/unlock", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: this.inputText2,
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    this.inputText1 = data.response;
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
        },
        sendMessage() {
            if (this.inputText3.trim() !== "") {
                fetch("/message", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        message: this.inputText3,
                    }),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        this.inputText3 = data.response;
                    })
                    .catch((error) => {
                        console.error("SendMessage Fail!", error);
                    })
            } else {
                alert("不能留言空内容！");
            }
        },
    },
});
