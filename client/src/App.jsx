import { useState, useEffect } from 'react'
import { getStrategies, runSimulation } from './api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Play, RotateCcw } from 'lucide-react';

function App() {
    const [strategies, setStrategies] = useState([]);
    const [p1, setP1] = useState('TitForTat');
    const [p2, setP2] = useState('RandomStrategy');
    const [rounds, setRounds] = useState(100);
    const [noise, setNoise] = useState(0.0);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        getStrategies().then(setStrategies);
    }, []);

    const handleRun = async () => {
        setLoading(true);
        try {
            const data = await runSimulation(p1, p2, rounds, noise);
            setResult(data);
        } catch (error) {
            console.error("Simulation failed:", error);
            alert("Simulation failed. Is the backend running?");
        }
        setLoading(false);
    };

    return (
        <div className="container">
            <header className="header">
                <h1>Prisoner's Dilemma Laboratory</h1>
                <p></p>
            </header>

            <div className="controls-card">
                <div className="control-group">
                    <label>Player 1 Strategy</label>
                    <select value={p1} onChange={(e) => setP1(e.target.value)}>
                        {strategies.map(s => <option key={s} value={s}>{s}</option>)}
                    </select>
                </div>

                <div className="control-group">
                    <label>Player 2 Strategy</label>
                    <select value={p2} onChange={(e) => setP2(e.target.value)}>
                        {strategies.map(s => <option key={s} value={s}>{s}</option>)}
                    </select>
                </div>

                <div className="control-group">
                    <label>Rounds</label>
                    <input type="number" value={rounds} onChange={(e) => setRounds(Number(e.target.value))} min="10" max="1000" />
                </div>

                <div className="control-group">
                    <label>Noise (Error Rate)</label>
                    <input type="number" value={noise} onChange={(e) => setNoise(Number(e.target.value))} min="0" max="1" step="0.05" />
                </div>

                <button className="btn" onClick={handleRun} disabled={loading}>
                    {loading ? 'Running...' : <><Play size={16} style={{ marginRight: '8px' }} /> Run Simulation</>}
                </button>
            </div>

            {result && (
                <div className="grid">
                    <div className="main-panel">
                        <div className="card">
                            <h2>Score Evolution</h2>
                            <div style={{ width: '100%', height: 300 }}>
                                <ResponsiveContainer>
                                    <LineChart data={result.log}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#30363d" />
                                        <XAxis dataKey="round" stroke="#8b949e" />
                                        <YAxis stroke="#8b949e" />
                                        <Tooltip contentStyle={{ backgroundColor: '#161b22', border: '1px solid #30363d' }} />
                                        <Legend />
                                        <Line type="monotone" dataKey="p1_score" stroke="#58a6ff" name={result.p1_name} dot={false} />
                                        <Line type="monotone" dataKey="p2_score" stroke="#da3633" name={result.p2_name} dot={false} />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        <div className="card">
                            <h2>Insight Analysis</h2>
                            <div className="explanation">
                                <p><strong>Result:</strong> {result.p1_score > result.p2_score ? result.p1_name : (result.p2_score > result.p1_score ? result.p2_name : "Tie")} won the match.</p>
                                <p><strong>Cooperation Rates:</strong> {result.p1_name}: {((result.p1_history.filter(m => m === 'C').length / result.rounds) * 100).toFixed(1)}% | {result.p2_name}: {((result.p2_history.filter(m => m === 'C').length / result.rounds) * 100).toFixed(1)}%</p>
                                {result.noise > 0 && <p><strong>Noise Impact:</strong> With {result.noise * 100}% noise, some moves were flipped, potentially breaking cooperative loops.</p>}
                            </div>
                        </div>
                    </div>

                    <div className="side-panel">
                        <div className="card">
                            <h2>Final Scores</h2>
                            <div className="metrics">
                                <div className="metric">
                                    <div className="metric-value">{result.p1_score}</div>
                                    <div>{result.p1_name}</div>
                                </div>
                                <div className="metric">
                                    <div className="metric-value">{result.p2_score}</div>
                                    <div>{result.p2_name}</div>
                                </div>
                            </div>
                        </div>

                        <div className="card">
                            <h2>Match Log</h2>
                            <div className="history-scroll">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>R</th>
                                            <th>{result.p1_name}</th>
                                            <th>{result.p2_name}</th>
                                            <th>Scores</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {result.log.map((log) => (
                                            <tr key={log.round}>
                                                <td>{log.round}</td>
                                                <td className={`move-${log.p1_move}`}>{log.p1_move}</td>
                                                <td className={`move-${log.p2_move}`}>{log.p2_move}</td>
                                                <td>{log.p1_score} - {log.p2_score}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
