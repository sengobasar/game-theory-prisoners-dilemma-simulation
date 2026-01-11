import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const getStrategies = async () => {
    const response = await axios.get(`${API_URL}/strategies`);
    return response.data.strategies;
};

export const runSimulation = async (p1Strategy, p2Strategy, rounds = 100, noise = 0.0) => {
    const response = await axios.post(`${API_URL}/simulation/run`, {
        p1_strategy: p1Strategy,
        p2_strategy: p2Strategy,
        rounds: rounds,
        noise: noise
    });
    return response.data;
};
