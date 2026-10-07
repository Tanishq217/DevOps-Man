import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const API_BASE = '/api';

function App() {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState({ total: 0, todo: 0, inProgress: 0, done: 0 });
  const [filter, setFilter] = useState('ALL');
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [systemHealth, setSystemHealth] = useState({ status: 'CHECKING', backend: 'ONLINE' });

  const loadData = async () => {
    try {
      setError('');
      const [tasksRes, statsRes] = await Promise.all([
        fetch(`${API_BASE}/tasks`),
        fetch(`${API_BASE}/tasks/stats`),
      ]);

      if (!tasksRes.ok || !statsRes.ok) {
        throw new Error('Backend API service temporarily unreachable');
      }

      const tasksData = await tasksRes.json();
      const statsData = await statsRes.json();
      setTasks(tasksData);
      setStats(statsData);
      setSystemHealth({ status: 'HEALTHY', backend: 'ONLINE' });
    } catch (err) {
      setError(err.message);
      setSystemHealth({ status: 'DEGRADED', backend: 'OFFLINE' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleAdvanceStatus = async (task) => {
    const nextStatusMap = {
      TODO: 'IN_PROGRESS',
      IN_PROGRESS: 'DONE',
      DONE: 'TODO',
    };
    const nextStatus = nextStatusMap[task.status] || 'TODO';

    try {
      const res = await fetch(`${API_BASE}/tasks/${task.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...task, status: nextStatus }),
      });
      if (res.ok) loadData();
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      const res = await fetch(`${API_BASE}/tasks/${taskId}`, {
        method: 'DELETE',
      });
      if (res.ok) loadData();
    } catch (err) {
      console.error('Failed to delete task:', err);
    }
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const payload = {
      title: formData.get('title'),
      description: formData.get('description'),
      priority: formData.get('priority'),
      assignee: formData.get('assignee') || 'Tanishq Singh',
      status: 'TODO',
    };

    try {
      const res = await fetch(`${API_BASE}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        e.currentTarget.reset();
        setShowModal(false);
        loadData();
      }
    } catch (err) {
      console.error('Failed to create task:', err);
    }
  };

  const visibleTasks = filter === 'ALL'
    ? tasks
    : tasks.filter((t) => t.status === filter);

  return (
    <div className="app">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div>
          <div className="brand">
            <span className="brand-mark">⚡</span>
            <div className="brand-text">
              <h2>TaskBoard</h2>
              <p>DevSecOps Capstone</p>
            </div>
          </div>
          <nav className="nav-links">
            <a className="nav-item active">
              <span>▦</span> Dashboard
            </a>
            <a className="nav-item">
              <span>✓</span> Tasks & Sprint
            </a>
            <a className="nav-item">
              <span>⚙</span> CI/CD Pipelines
            </a>
            <a className="nav-item">
              <span>🔒</span> Security Gates
            </a>
            <a className="nav-item">
              <span>📈</span> Metrics & Logs
            </a>
          </nav>
        </div>

        <div className="sidebar-footer">
          <div className="capstone-badge">
            <strong>Production Cluster</strong>
            <span>Kubernetes v1.31 + Helm</span>
            <div style={{ marginTop: '0.35rem', color: '#10b981', fontSize: '0.75rem' }}>
              ● Backend: {systemHealth.backend}
            </div>
          </div>
          <div className="profile-card">
            <div className="avatar">TS</div>
            <div className="profile-info">
              <b>Tanishq Singh</b>
              <small>DevOps Lead | 24bcs10303</small>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main">
        <header className="header">
          <div>
            <p className="eyebrow">ENTERPRISE WORKSPACE / CLOUD PLATFORM</p>
            <h1>Good morning, Tanishq 👋</h1>
            <p className="subtitle">
              End-to-End DevSecOps, Kubernetes, Terraform & Observability Dashboard.
            </p>
          </div>
          <button className="btn-primary" onClick={() => setShowModal(true)}>
            <span>＋</span> Create Task
          </button>
        </header>

        {error && (
          <div className="alert">
            ⚠️ {error}. Ensure backend container (FastAPI) and PostgreSQL/SQLite are operational.
          </div>
        )}

        {/* Top KPI Stat Cards */}
        <section className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon blue">▦</div>
            <div className="stat-content">
              <small>Total Tasks</small>
              <strong>{stats.total}</strong>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon yellow">○</div>
            <div className="stat-content">
              <small>To Do (Backlog)</small>
              <strong>{stats.todo}</strong>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon purple">◔</div>
            <div className="stat-content">
              <small>In Progress</small>
              <strong>{stats.inProgress}</strong>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon green">✓</div>
            <div className="stat-content">
              <small>Completed</small>
              <strong>{stats.done}</strong>
            </div>
          </div>
        </section>

        {/* Content Layout */}
        <section className="content-grid">
          {/* Tasks Table Panel */}
          <div className="panel">
            <div className="panel-header">
              <div className="panel-title">
                <h2>Active Task Items</h2>
                <p>Real-time synchronisation with PostgreSQL & REST APIs.</p>
              </div>
              <div className="filter-group">
                {['ALL', 'TODO', 'IN_PROGRESS', 'DONE'].map((mode) => (
                  <button
                    key={mode}
                    className={`filter-btn ${filter === mode ? 'active' : ''}`}
                    onClick={() => setFilter(mode)}
                  >
                    {mode === 'ALL' ? 'All' : mode.replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>

            {loading ? (
              <div style={{ textAlign: 'center', padding: '3rem', color: '#9ca3af' }}>
                Connecting to TaskBoard API service...
              </div>
            ) : (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Task Title</th>
                      <th>Assignee</th>
                      <th>Priority</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {visibleTasks.map((t) => (
                      <tr key={t.id}>
                        <td>
                          <div className="task-item">
                            <span className={`status-dot ${t.status.toLowerCase()}`}></span>
                            <div>
                              <strong>{t.title}</strong>
                              <span className="task-desc">{t.description || 'No description provided'}</span>
                            </div>
                          </div>
                        </td>
                        <td>{t.assignee}</td>
                        <td>
                          <span className={`badge badge-${t.priority.toLowerCase()}`}>
                            {t.priority}
                          </span>
                        </td>
                        <td>
                          <span className={`badge-status ${t.status.toLowerCase()}`}>
                            {t.status.replace('_', ' ')}
                          </span>
                        </td>
                        <td>
                          <div className="actions-cell">
                            <button
                              className="btn-icon"
                              onClick={() => handleAdvanceStatus(t)}
                              title="Advance Status"
                            >
                              ↻
                            </button>
                            <button
                              className="btn-icon danger"
                              onClick={() => handleDeleteTask(t.id)}
                              title="Delete Task"
                            >
                              ✕
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {!visibleTasks.length && (
                  <div style={{ textAlign: 'center', padding: '3rem', color: '#9ca3af' }}>
                    No tasks found in filter "{filter}".
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Right Sidebar: Pipeline & Activity Feed */}
          <aside className="panel">
            <div className="panel-header">
              <div className="panel-title">
                <h2>DevSecOps Feed</h2>
                <p>CI/CD pipeline telemetry & activity.</p>
              </div>
            </div>

            <div className="activity-list">
              <div className="activity-item">
                <span className="activity-icon">✓</span>
                <div className="activity-details">
                  <b>GitHub Actions Workflow</b>
                  <small>Passed 9 pipeline stages in 1m 24s</small>
                </div>
              </div>
              <div className="activity-item">
                <span className="activity-icon">🔒</span>
                <div className="activity-details">
                  <b>Trivy Security Gate</b>
                  <small>0 CRITICAL CVEs detected</small>
                </div>
              </div>
              <div className="activity-item">
                <span className="activity-icon">☸</span>
                <div className="activity-details">
                  <b>Kubernetes Deployment</b>
                  <small>2/2 Pods Ready across cluster</small>
                </div>
              </div>
              <div className="activity-item">
                <span className="activity-icon">📊</span>
                <div className="activity-details">
                  <b>Prometheus /metrics</b>
                  <small>Scraping HTTP latency & counters</small>
                </div>
              </div>
            </div>

            <div className="pipeline-widget">
              <div className="pipeline-title">Delivery Pipeline Flow</div>
              <div className="pipeline-steps">
                <div className="step-node">Git Push</div>
                <span className="step-arrow">→</span>
                <div className="step-node">SAST/SCA</div>
                <span className="step-arrow">→</span>
                <div className="step-node">Trivy</div>
                <span className="step-arrow">→</span>
                <div className="step-node">K8s Rollout</div>
              </div>
            </div>
          </aside>
        </section>

        {/* Create Task Modal */}
        {showModal && (
          <div className="modal-overlay" onClick={() => setShowModal(false)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h3>Create New Task</h3>
                <button className="modal-close" onClick={() => setShowModal(false)}>
                  ×
                </button>
              </div>
              <form onSubmit={handleCreateTask}>
                <div className="form-group">
                  <label>Task Title *</label>
                  <input
                    name="title"
                    required
                    className="form-control"
                    placeholder="e.g., Configure Ingress Controller"
                  />
                </div>
                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    name="description"
                    className="form-control"
                    placeholder="Provide context and requirements..."
                  />
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Priority</label>
                    <select name="priority" className="form-control">
                      <option value="LOW">LOW</option>
                      <option value="MEDIUM">MEDIUM</option>
                      <option value="HIGH">HIGH</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Assignee</label>
                    <input
                      name="assignee"
                      defaultValue="Tanishq Singh"
                      className="form-control"
                    />
                  </div>
                </div>
                <button type="submit" className="btn-primary btn-full">
                  Save & Deploy Task
                </button>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);
