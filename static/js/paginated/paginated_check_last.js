check_last = function()
{
    var cur_page = document.getElementById("jumpWhere").value;
    var a_next =document.getElementById("nextpage");
    var o_select = document.getElementById("jumpWhere");
    var total_page = o_select.length;
    if(cur_page==total_page) {
        a_next.href = "#";
        alert("当前已在最后一页！");
    }
}