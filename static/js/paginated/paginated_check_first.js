check_first = function()
{
    var cur_page = document.getElementById("jumpWhere").value;
    var a_pre =document.getElementById("prepage");

    if (cur_page==1) {
        a_pre.href = "/page/".concat(1);
        alert("当前已在第一页！");
    }
}