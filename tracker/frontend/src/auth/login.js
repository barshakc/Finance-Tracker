import { useState } from 'react';
import api from '../api/axios';

export default function Login(){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async (e)=>{
        e.preventDefault();

        const res =await api.post("/auth/login/", {
            username,
            password,
        });

        localStorage.setItem('access', res.data.access);
        localStorage.setItem('refresh', res.data.refresh);

        window.location.href = '/dashboard';
    };

    return(
      <form onSubmit={handleLogin}>
        <input placeholder="username" onChange={e => setUsername(e.target.value)} />
        <input type="password" placeholder="password" onChange={e => setPassword(e.target.value)} />
        <button type="submit">Login</button>
      </form>
    );
        
}

