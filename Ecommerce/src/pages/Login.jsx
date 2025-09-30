import React, { useState } from 'react';

const Login = () => {
   
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('');

        
        const BACKEND_URL = 'http://localhost:5000/api/login'; 

        try {
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
             
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                setMessage(`Login realizado com sucesso! Bem-vindo(a), ${data.username || 'Usuário'}.`);
              
            } else {
                setMessage(data.error || 'Credenciais inválidas. Tente novamente.');
            }
        } catch (error) {
            setMessage('Ocorreu um erro ao conectar com o servidor. Verifique se o backend está ativo.');
            console.error('Erro de conexão:', error);
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Senha:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Entrar</button>
            </form>
            {message && <p style={{ color: message.includes('sucesso') ? 'green' : 'red' }}>{message}</p>}
        </div>
    );
};

export default Login;
