async function handleClick(nuevo_rol) {
    var table = document.getElementById('users')
    var tbody = table.getElementsByTagName('tbody')[0]
    var rows = tbody.getElementsByTagName('tr');
    for (i = 0; i < rows.length; i++) {
        rows[i].onclick = function() {
        console.log(this.rowIndex)
        document.querySelector('input[name="ID"]').value = this.rowIndex;
        document.querySelector('input[name="rol"]').value = nuevo_rol;
        document.getElementById('update-form').submit();
        }
    }
}