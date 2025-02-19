function confirmDelete(id) {
    if (confirm('Yakin mau hapus?')) {
        fetch(`/hapus_pesanan/${id}`, { method: 'POST' })
            .then(response => window.location.href = '/dashboard')
            .catch(error => console.error('Error:', error));
    }
}

function confirmSelesai(id) {
    if (confirm('Yakin selesai?')) {
        fetch(`/selesai_pesanan/${id}`, { method: 'POST' })
            .then(response => window.location.href = '/dashboard')
            .catch(error => console.error('Error:', error));
    }
}
