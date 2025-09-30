import React, { useState } from 'react';

const CreateProduct = () => {
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        price: '',
        image_url: ''
    });
    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('');

        
        const dataToSend = { ...formData, price: parseFloat(formData.price) };

        try {
            const response = await fetch('http://localhost:5000/api/products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include', 
                
                body: JSON.stringify(dataToSend),
            });

            const data = await response.json();

            if (response.status === 201) {
                setMessage(`Produto "${dataToSend.name}" registrado com sucesso! ID: ${data.product_id}`);
                setFormData({ name: '', text: '', price: '', image_url: '' }); 
            } else if (response.status === 401) {
                setMessage('Acesso negado. Você precisa estar logado para registrar um produto.');
            } 
            else {
                setMessage(data.error || 'Erro ao registrar o produto. Verifique os campos.');
            }
        } catch (error) {
            setMessage('Erro de conexão. Verifique se o servidor backend está ativo.');
            console.error('Erro de conexão:', error);
        }
    };

    return (
        <div>
            <h2>Registrar Novo Produto</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Nome do Produto:</label>
                    <input type="text" name="name" value={formData.name} onChange={handleChange} required />
                </div>
                <div>
                    <label>Descrição:</label>
                    <textarea name="text" value={formData.text} onChange={handleChange} required></textarea>
                </div>
                <div>
                    <label>Preço (R$):</label>
                    <input type="number" name="price" value={formData.price} onChange={handleChange} required step="0.01" />
                </div>
                <div>
                    <label>URL da Imagem:</label>
                    <input type="url" name="image_url" value={formData.image_url} onChange={handleChange} required />
                </div>
                <button type="submit">Registrar Produto</button>
            </form>
            {message && <p style={{ color: message.includes('sucesso') ? 'green' : 'red', marginTop: '15px' }}>{message}</p>}
        </div>
    );
};

export default CreateProduct;