import { useState, useEffect } from "react";
import "./Transactions.css";

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTransactions();
    const interval = setInterval(fetchTransactions, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchTransactions = async () => {
    setLoading(true);
    const txns = [];
    setTransactions(txns);
    setLoading(false);
  };

  return (
    <div className="transactions-page">
      <div className="transactions-container">
        <h1 className="page-title">Credit Transactions</h1>
        <p className="page-subtitle">View your credit transaction history</p>

        {loading ? (
          <p className="loading-state">Loading transactions...</p>
        ) : transactions.length === 0 ? (
          <p className="empty-state">No transactions yet</p>
        ) : (
          <div className="transactions-table">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Type</th>
                  <th>Job ID</th>
                  <th>Amount</th>
                  <th>Balance</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((txn, idx) => (
                  <tr key={idx}>
                    <td>{new Date(txn.timestamp).toLocaleString()}</td>
                    <td>
                      <span className={`txn-type ${txn.type}`}>
                        {txn.type}
                      </span>
                    </td>
                    <td className="job-id">{txn.job_id}</td>
                    <td className={txn.amount > 0 ? "positive" : "negative"}>
                      {txn.amount > 0 ? "+" : ""}${txn.amount}
                    </td>
                    <td>${txn.balance}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Transactions;
