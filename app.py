from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'una_clave_secreta'

def generar_id_producto():
    if 'productos' in session and session['productos']:
        return max(item['id'] for item in session['productos']) + 1
    return 1

@app.route('/')
def index():
    if 'productos' not in session:
        session['productos'] = []

    productos = session.get('productos', [])
    return render_template('index.html', productos=productos)

@app.route('/nuevo', methods=['POST', 'GET'])
def nuevo():
    if request.method == 'POST':
        nombre_producto = request.form['nombre']
        cantidad_producto = request.form['cantidad']
        precio_producto = request.form['precio']
        fecha_producto = request.form['fec_producto']
        categoria_producto = request.form['categoria']

        nuevo_producto = {
            'id': generar_id_producto(),
            'nombre': nombre_producto,
            'cantidad': cantidad_producto,
            'precio': precio_producto,
            'fec_producto': fecha_producto,
            'categoria': categoria_producto,
        }

        if 'productos' not in session:
            session['productos'] = []

        session['productos'].append(nuevo_producto)
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('nuevo.html')

@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar(id):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == id), None)
    if not producto:
        return redirect(url_for('index'))

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = request.form['cantidad']
        producto['precio'] = request.form['precio']
        producto['fec_producto'] = request.form['fec_producto']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))

    return render_template('editar.html', producto=producto)

@app.route('/eliminar/<int:id>', methods=['POST', 'GET'])
def eliminar(id):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == id), None)
    if producto:
        session['productos'].remove(producto)
        session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
