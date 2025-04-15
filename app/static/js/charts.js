// Wait for the DOM to load before executing
document.addEventListener("DOMContentLoaded", function() {
    // Get the data for the pie charts from the server (you'll pass this data from Flask to the frontend)
    var expenseLabels = JSON.parse(document.getElementById("expense-labels").textContent);
    var expenseValues = JSON.parse(document.getElementById("expense-values").textContent);
    var totalBudget = parseFloat(document.getElementById("total-budget").textContent);
    var totalExpenses = parseFloat(document.getElementById("total-expenses").textContent);
    
    // Remaining budget
    var remainingBudget = totalBudget - totalExpenses;

    // Create the Remaining Budget vs Expenses Pie Chart
    var ctx1 = document.getElementById('remainingBudgetChart').getContext('2d');
    new Chart(ctx1, {
        type: 'pie',
        data: {
            labels: ['Remaining Budget', 'Expenses'],
            datasets: [{
                data: [remainingBudget, totalExpenses],
                backgroundColor: ['#4CAF50', '#FF6347'],
                borderColor: ['#2E7D32', '#D32F2F'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return '$' + tooltipItem.raw.toFixed(2);
                        }
                    }
                }
            }
        }
    });

    // Create the Distribution of Expenses by Category Pie Chart
    var ctx2 = document.getElementById('expenseDistributionChart').getContext('2d');
    new Chart(ctx2, {
        type: 'pie',
        data: {
            labels: expenseLabels,
            datasets: [{
                data: expenseValues,
                backgroundColor: ['#FF5733', '#33FF57', '#3357FF', '#FFC300', '#FF33F6'],
                borderColor: ['#C70039', '#28B463', '#1D4D94', '#F39C12', '#F12C80'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return '$' + tooltipItem.raw.toFixed(2);
                        }
                    }
                }
            }
        }
    });
});
