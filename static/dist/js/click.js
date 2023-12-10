document.querySelectorAll('.alertbutton').forEach(function(button) {
    button.onclick = function() {
       var answer = confirm('Hai! Apakah Anda yakin akan menghapus pilihan basis pengetahuan ini?');
       if (answer) {
         alert('Basis pengetahuan yang anda pilih berhasil dihapus!');
       } else {
         alert('Basis pengetahuan yang anda pilih gagal dihapus!');
       }
    }
});

