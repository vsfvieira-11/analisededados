import React, { useMemo, useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

const datasets = [
  {
    key: 'enxofre',
    label: 'Enxofre',
    defaultMetric: 'enxofre',
    description: 'Fluxo completo de preparação, modelagem e análise de resíduos para o conjunto de enxofre.',
    steps: [
      { title: '1. data_enxofre.py', description: 'Gera a tabela combinada a partir dos espectros e das propriedades.', file: 'Enxofre/data_enxofre.py' },
      { title: '2. modelo_enxofre.py', description: 'Constrói o modelo e gera os gráficos de avaliação.', file: 'Enxofre/modelo_enxofre.py' },
      { title: '3. modelo_enxofre_soutliers.py', description: 'Reexecuta a modelagem com análise de outliers.', file: 'Enxofre/modelo_enxofre_soutliers.py' },
      { title: '4. data_enxofre_VIP_soutlier.py', description: 'Filtra amostras com base em VIP e outliers.', file: 'Enxofre/data_enxofre_VIP_soutlier.py' },
      { title: '5. calculo_residuos_enxofre.py', description: 'Calcula resíduos e métricas associadas.', file: 'Enxofre/calculo_residuos_enxofre.py' },
    ],
    csvPath: '/data/pca_dataset.csv',
    pcaPath: '/data/scores_pca.csv',
    loadingsPath: '/data/loadings.csv',
  },
  {
    key: 'fulgor',
    label: 'Fulgor',
    defaultMetric: 'ponto de fulgor',
    description: 'Painel para o conjunto de fulgor, incluindo PCA, histogramas e análise de distribuição das propriedades.',
    steps: [
      { title: '1. data_fulgor.py', description: 'Gera a tabela combinada a partir dos espectros e das propriedades.', file: 'Fulgor/data_fulgor.py' },
      { title: '2. modelo_fulgor.py', description: 'Constrói o modelo e gera os gráficos de avaliação.', file: 'Fulgor/modelo_fulgor.py' },
      { title: '3. modelo_fulgor_soutliers.py', description: 'Reexecuta a modelagem com análise de outliers.', file: 'Fulgor/modelo_fulgor_soutliers.py' },
      { title: '4. data_fulgor_VIP_soutlier.py', description: 'Filtra amostras com base em VIP e outliers.', file: 'Fulgor/data_fulgor_VIP_soutlier.py' },
      { title: '5. calculo_residuos_fulgor.py', description: 'Calcula resíduos e métricas associadas.', file: 'Fulgor/calculo_residuos_fulgor.py' },
    ],
    csvPath: '/data/pca_dataset.csv',
    pcaPath: '/data/scores_pca.csv',
    loadingsPath: '/data/loadings.csv',
  },
  {
    key: 'massa',
    label: 'Massa específica',
    defaultMetric: 'massa especifica',
    description: 'Painel para o conjunto de massa específica com visão integrada de PCA, distribuição e fluxo do projeto.',
    steps: [
      { title: '1. data_massa_esp.py', description: 'Gera a tabela combinada a partir dos espectros e das propriedades.', file: 'Massa_esp/data_massa_esp.py' },
      { title: '2. modelo_massa_esp.py', description: 'Constrói o modelo e gera os gráficos de avaliação.', file: 'Massa_esp/modelo_massa_esp.py' },
      { title: '3. modelo_massa_esp_soutliers.py', description: 'Reexecuta a modelagem com análise de outliers.', file: 'Massa_esp/modelo_massa_esp_soutliers.py' },
      { title: '4. data_massa_esp_VIP_soutlier.py', description: 'Filtra amostras com base em VIP e outliers.', file: 'Massa_esp/data_massa_esp_VIP_soutlier.py' },
      { title: '5. calculo_residuos_massa_esp.py', description: 'Calcula resíduos e métricas associadas.', file: 'Massa_esp/calculo_residuos_massa_esp.py' },
    ],
    csvPath: '/data/pca_dataset.csv',
    pcaPath: '/data/scores_pca.csv',
    loadingsPath: '/data/loadings.csv',
  },
];

const metricOptions = [
  { value: 'ponto de fulgor', label: 'Ponto de fulgor' },
  { value: 'massa especifica', label: 'Massa específica' },
  { value: 'enxofre', label: 'Enxofre' },
];

const parseNumber = (value) => {
  if (value === null || value === undefined || value === '') return null;
  const normalized = String(value).trim().replace(/\./g, '').replace(',', '.');
  const numeric = Number(normalized);
  return Number.isFinite(numeric) ? numeric : null;
};

const loadCsv = async (path) => {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Falha ao carregar ${path}`);
  const text = await response.text();
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  const delimiter = lines.some((line) => line.includes(';')) ? ';' : ',';
  const headers = lines[0].split(delimiter);
  return lines.slice(1).map((line) => {
    const values = line.split(delimiter);
    const row = {};
    headers.forEach((header, index) => {
      row[header] = values[index] ?? '';
    });
    return row;
  });
};

function App() {
  const [activeTab, setActiveTab] = useState('enxofre');
  const [datasetData, setDatasetData] = useState([]);
  const [pcaData, setPcaData] = useState([]);
  const [loadingsData, setLoadingsData] = useState([]);
  const [selectedMetric, setSelectedMetric] = useState('ponto de fulgor');
  const [isLoading, setIsLoading] = useState(true);

  const activeDataset = datasets.find((item) => item.key === activeTab) ?? datasets[0];

  useEffect(() => {
    let active = true;
    setIsLoading(true);
    setSelectedMetric(activeDataset.defaultMetric);
    Promise.all([
      loadCsv(activeDataset.csvPath),
      loadCsv(activeDataset.pcaPath),
      loadCsv(activeDataset.loadingsPath),
    ])
      .then(([dataset, pca, loadings]) => {
        if (!active) return;
        setDatasetData(dataset);
        setPcaData(pca);
        setLoadingsData(loadings);
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        if (active) setIsLoading(false);
      });
    return () => { active = false; };
  }, [activeDataset.key]);

  const summary = useMemo(() => {
    const numericMetrics = datasetData
      .map((row) => parseNumber(row[selectedMetric]))
      .filter((value) => value !== null);

    const values = numericMetrics.length ? numericMetrics : [0];
    const min = Math.min(...values);
    const max = Math.max(...values);
    const avg = values.reduce((acc, value) => acc + value, 0) / values.length;

    return {
      amostras: datasetData.length,
      metric: selectedMetric,
      min: min.toFixed(2),
      max: max.toFixed(2),
      avg: avg.toFixed(2),
    };
  }, [datasetData, selectedMetric]);

  const histogramData = useMemo(() => {
    return datasetData
      .map((row) => parseNumber(row[selectedMetric]))
      .filter((value) => value !== null);
  }, [datasetData, selectedMetric]);

  const scatterData = useMemo(() => {
    return pcaData
      .map((row) => ({
        amostra: row.amostra,
        x: parseNumber(row.PC1),
        y: parseNumber(row.PC2),
        value: parseNumber(row[selectedMetric]),
      }))
      .filter((row) => row.x !== null && row.y !== null);
  }, [pcaData, selectedMetric]);

  const loadingSeries = useMemo(() => {
    return loadingsData
      .map((row) => {
        const keys = Object.keys(row).filter((key) => key !== 'Unnamed: 0' && key !== '0');
        return {
          name: row['Unnamed: 0'] || row['0'] || 'Variável',
          x: keys,
          y: keys.map((key) => parseNumber(row[key]) || 0),
        };
      })
      .filter((row) => row.x.length > 0);
  }, [loadingsData]);

  const tableRows = useMemo(() => {
    return datasetData.slice(0, 10).map((row) => ({
      amostra: row.amostra || row.codigo || '-',
      pontoFulgor: row['ponto de fulgor'] || '-',
      massaEspecifica: row['massa especifica'] || '-',
      enxofre: row.enxofre || '-',
    }));
  }, [datasetData]);

  const activeMetricLabel = metricOptions.find((option) => option.value === selectedMetric)?.label || selectedMetric;

  return (
    <div className="app-shell">
      <header className="hero">
        <h1>Dashboard interativo do projeto</h1>
        <p>Interface modular em abas para explorar os fluxos de Enxofre, Fulgor e Massa específica com PCA, distribuição das propriedades, tabela de amostras e passos do fluxo.</p>
      </header>

      <nav className="tabs">
        {datasets.map((dataset) => (
          <button
            key={dataset.key}
            className={`tab-button ${activeTab === dataset.key ? 'active' : ''}`}
            onClick={() => setActiveTab(dataset.key)}
          >
            {dataset.label}
          </button>
        ))}
      </nav>

      <section className="panel">
        <div className="controls">
          <div>
            <h2 style={{ margin: '0 0 6px' }}>{activeDataset.label}</h2>
            <p style={{ margin: 0, color: '#9fb5d2' }}>{activeDataset.description}</p>
          </div>
          <div className="select-wrap">
            <label htmlFor="metric">Métrica em análise</label>
            <select id="metric" value={selectedMetric} onChange={(event) => setSelectedMetric(event.target.value)}>
              {metricOptions.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="summary-grid">
          <div className="summary-card">
            <div className="label">Amostras carregadas</div>
            <div className="value">{isLoading ? '...' : summary.amostras}</div>
          </div>
          <div className="summary-card">
            <div className="label">Métrica selecionada</div>
            <div className="value">{activeMetricLabel}</div>
          </div>
          <div className="summary-card">
            <div className="label">Mínimo</div>
            <div className="value">{summary.min}</div>
          </div>
          <div className="summary-card">
            <div className="label">Máximo</div>
            <div className="value">{summary.max}</div>
          </div>
          <div className="summary-card">
            <div className="label">Média</div>
            <div className="value">{summary.avg}</div>
          </div>
        </div>

        <div className="chart-grid">
          <div className="chart-card">
            <Plot
              data={[
                {
                  x: histogramData,
                  type: 'histogram',
                  marker: { color: '#5c8dff' },
                  name: activeMetricLabel,
                },
              ]}
              layout={{
                title: `Histograma de ${activeMetricLabel} — todas as amostras do conjunto ${activeDataset.label}`,
                template: 'plotly_white',
                margin: { l: 40, r: 20, t: 50, b: 40 },
                bargap: 0.05,
                xaxis: { title: activeMetricLabel },
                yaxis: { title: 'Frequência' },
              }}
              useResizeHandler
              style={{ width: '100%', height: '100%' }}
            />
          </div>
          <div className="chart-card">
            <Plot
              data={[
                {
                  x: scatterData.map((point) => point.x),
                  y: scatterData.map((point) => point.y),
                  text: scatterData.map((point) => point.amostra),
                  mode: 'markers',
                  marker: {
                    size: 10,
                    color: scatterData.map((point) => point.value),
                    colorscale: 'Viridis',
                    showscale: true,
                  },
                  type: 'scatter',
                  name: 'Scores PCA',
                },
              ]}
              layout={{
                title: `PCA completo para ${activeDataset.label} — scores PC1 x PC2 com todas as amostras`,
                template: 'plotly_white',
                margin: { l: 40, r: 20, t: 50, b: 40 },
                xaxis: { title: 'PC1' },
                yaxis: { title: 'PC2' },
                hovermode: 'closest',
              }}
              useResizeHandler
              style={{ width: '100%', height: '100%' }}
            />
          </div>
        </div>

        <div className="chart-grid">
          <div className="chart-card">
            <Plot
              data={loadingSeries.map((series) => ({
                x: series.x,
                y: series.y,
                type: 'bar',
                name: series.name,
              }))}
              layout={{
                title: `Loadings do PCA — contribuição das variáveis para ${activeDataset.label}`,
                template: 'plotly_white',
                margin: { l: 40, r: 20, t: 50, b: 40 },
                barmode: 'group',
              }}
              useResizeHandler
              style={{ width: '100%', height: '100%' }}
            />
          </div>
          <div className="chart-card">
            <Plot
              data={[
                {
                  y: histogramData,
                  type: 'box',
                  name: activeMetricLabel,
                  boxpoints: 'all',
                  jitter: 0.3,
                  pointpos: -1.8,
                  marker: { color: '#ff8a5b' },
                },
              ]}
              layout={{
                title: `Boxplot da distribuição de ${activeMetricLabel} em ${activeDataset.label}`,
                template: 'plotly_white',
                margin: { l: 40, r: 20, t: 50, b: 40 },
                yaxis: { title: activeMetricLabel },
              }}
              useResizeHandler
              style={{ width: '100%', height: '100%' }}
            />
          </div>
        </div>

        <div className="table-card">
          <h3>Visualização das primeiras amostras</h3>
          <p>Esta tabela permite inspecionar rapidamente os primeiros registros carregados a partir do arquivo de dados.</p>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Amostra</th>
                  <th>Ponto de fulgor</th>
                  <th>Massa específica</th>
                  <th>Enxofre</th>
                </tr>
              </thead>
              <tbody>
                {tableRows.map((row) => (
                  <tr key={row.amostra}>
                    <td>{row.amostra}</td>
                    <td>{row.pontoFulgor}</td>
                    <td>{row.massaEspecifica}</td>
                    <td>{row.enxofre}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="step-grid">
          {activeDataset.steps.map((step) => (
            <div key={step.title} className="step-card">
              <h4>{step.title}</h4>
              <p>{step.description}</p>
              <code>{step.file}</code>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;
