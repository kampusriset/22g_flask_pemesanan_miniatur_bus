from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pemesanan_miniatur_bis'
mysql = MySQL(app)

# Routes
@app.route('/')
def home():
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        mysql.connection.commit()
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pesanan WHERE status = "diproses"')
        pesanan_diproses = cursor.fetchall()
        cursor.execute('SELECT * FROM pesanan WHERE status = "selesai"')
        pesanan_selesai = cursor.fetchall()
        return render_template('dashboard.html', pesanan_diproses=pesanan_diproses, pesanan_selesai=pesanan_selesai)
    return redirect(url_for('login'))
def dashboard():
    pesanan_diproses = [
        {"id": 1, "nama": "Pesanan A"},
        {"id": 2, "nama": "Pesanan B"}
    ]
    
    pesanan_selesai = [
        {"id": 3, "nama": "Pesanan C"},
        {"id": 4, "nama": "Pesanan D"}
    ]

    return render_template('dashboard.html', pesanan_diproses=pesanan_diproses, pesanan_selesai=pesanan_selesai)

@app.route('/edit_pesanan/<int:id>', methods=['GET', 'POST'])
def edit_pesanan(id):
    if 'loggedin' in session:
        if request.method == 'POST':
            nama_pemesan = request.form['nama_pemesan']
            jenis_bus = request.form['jenis_bus']
            jumlah_pesanan = request.form['jumlah_pesanan']
            nomor_telepon = request.form['nomor_telepon']
            alamat = request.form['alamat']
            cursor = mysql.connection.cursor()
            cursor.execute('''
                UPDATE pesanan 
                SET nama_pemesan = %s, jenis_bus = %s, jumlah_pesanan = %s, nomor_telepon = %s, alamat = %s 
                WHERE id = %s
            ''', (nama_pemesan, jenis_bus, jumlah_pesanan, nomor_telepon, alamat, id))
            mysql.connection.commit()
            flash('Pesanan berhasil diupdate!', 'success')
            return redirect(url_for('dashboard'))
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM pesanan WHERE id = %s', (id,))
            pesanan = cursor.fetchone()
            return render_template('edit_pesanan.html', pesanan=pesanan)
    return redirect(url_for('login'))

@app.route('/hapus_pesanan/<int:id>', methods=['POST'])
def hapus_pesanan(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM pesanan WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    flash('Pesanan berhasil dihapus!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/selesai_pesanan/<int:id>', methods=['POST'])
def selesai_pesanan(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE pesanan SET status = "selesai" WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    flash('Pesanan berhasil diselesaikan!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/tambah_pesanan', methods=['GET', 'POST'])
def tambah_pesanan():
    if 'loggedin' in session:
        if request.method == 'POST':
            nama_pemesan = request.form['nama_pemesan']
            jenis_bus = request.form['jenis_bus']
            jumlah_pesanan = request.form['jumlah_pesanan']
            nomor_telepon = request.form['nomor_telepon']
            alamat = request.form['alamat']
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO pesanan (nama_pemesan, jenis_bus, jumlah_pesanan, nomor_telepon, alamat) VALUES (%s, %s, %s, %s, %s)', (nama_pemesan, jenis_bus, jumlah_pesanan, nomor_telepon, alamat))
            mysql.connection.commit()
            flash('Pesanan berhasil ditambahkan!', 'success')
            return redirect(url_for('dashboard'))
        return render_template('tambah_pesanan.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
