window.onbeforeunload = function () {
    var scrollPos;
    if (typeof window.pageYOffset != 'undefined') {
        scrollPos = window.pageYOffset;
    } else if (typeof document.compatMode != 'undefined' &&
        document.compatMode != 'BackCompat') {
        scrollPos = document.documentElement.scrollTop;
    } else if (typeof document.body != 'undefined') {
        scrollPos = document.body.scrollTop;
    }
    document.cookie = "scrollTop=" + scrollPos; //存储滚动条位置到cookies中
}

window.onload = function () {
    if (document.cookie.match(/scrollTop=([^;]+)(;|$)/) != null) {
        var arr = document.cookie.match(/scrollTop=([^;]+)(;|$)/); //cookies中不为空，则读取滚动条位置
        document.documentElement.scrollTop = parseInt(arr[1]);
        document.body.scrollTop = parseInt(arr[1]);
    }
}

function del(id) {
    /* 显示 */
    document.getElementById("delete" + id).style.display = "block";
}

function delesc(id) {
    /* 隐藏 */
    document.getElementById("delete" + id).style.display = "none";
}

/**
* 功能：post方式提交
* 参数列表：url：提交的地址；params：参数列表
*/
    function post(url, params) {
    var temp = document.createElement("form"); //创建form表单
    temp.action = url;
    temp.method = "post";
    temp.style.display = "none";//表单样式为隐藏
    for (var item in params) {//初始化表单内部的控件
       //根据实际情况创建不同的标签元素
        var opt =document.createElement("input");  //添加input标签
        opt.type="text";   //类型为text
        opt.id = item;      //设置id属性
        opt.name = item;    //设置name属性
        opt.value = params[item];   //设置value属性
        temp.appendChild(opt);
    }

    document.body.appendChild(temp);
    temp.submit();
    return temp;
}


