setAddress_jumpPage = function()
{
    var cur_page = document.getElementById("jumpWhere").value;
    var a_jump =document.getElementById("jumpPage");
    a_jump.href = "/page/".concat(cur_page).concat("{{schfilter}}");
}