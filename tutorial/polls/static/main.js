new Vue({
    el: "#app",
    data: {
        username: "",
        password: "",
        showLogin: false,
        showRegister: false,
        showPolls: true,
    },
    created() {
        this.CheckLogin();
    },
    methods: {
        CheckLogin: function () {
            that = this;
            axios({
                method: 'get',
                url: location.origin + '/questions',
                responseType: 'json'
            }).then(function(response){
                if (response.data === "no login") {
                    that.showLogin = true;
                    that.showRegister = false;
                    that.showPolls = false;
                }
            })
        },
        GetQuestionsHandle: function () {
            axios({
                method: 'get',
                url: location.origin + '/questions',
                responseType: 'json'
            }).then(function (response) {
                console.log(response);
            });
        },
        LoginHandle: function(){
            this.showLogin = true;
            this.showRegister = false;
            this.showPolls = false;
            console.log(this.username, this.password);
            that = this;
            axios({
                method: 'post',
                url: location.origin + '/login',
                data: {
                    username: this.username,
                    password: this.password,
                },
                responseType: 'json'
            }).then(function(response){
                if (response.data.status === true) {
                    that.showLogin = false;
                    that.showRegister = false;
                    that.showPolls = true;
                }
            })
        },
        RegisterHandle: function(){
            this.showLogin = false;
            this.showRegister = true;
            this.showPolls = false;
            console.log(this.username, this.password);
            that = this;
            axios({
                method: 'post',
                url: location.origin + '/register',
                data: {
                    username: this.username,
                    password: this.password,
                },
                responseType: 'json'
            }).then(function(response){
                if (response.data.status === true) {
                    that.showLogin = false;
                    that.showRegister = false;
                    that.showPolls = true;
                }
            })
        }
    }
})