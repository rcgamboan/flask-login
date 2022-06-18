function handleclick(id){
    $(id).on('click', function(e){
        var id = $(e.target).closest('tr').find(".id").html();
        console.log(id)
        })
}