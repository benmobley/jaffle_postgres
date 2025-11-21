import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
from sqlalchemy import create_engine
import os

# Page config
st.set_page_config(
    page_title="Olist Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection
@st.cache_resource
def get_database_connection():
    """Create database connection using environment variables"""
    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    db_name = os.getenv('POSTGRES_DB', 'jaffle')
    db_user = os.getenv('POSTGRES_USER', 'postgres')
    db_password = os.getenv('POSTGRES_PASSWORD', 'postgres')

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(connection_string)

@st.cache_data
def load_data(query):
    """Load data from database with caching"""
    engine = get_database_connection()
    return pd.read_sql(query, engine)

# Main dashboard
def main():
    st.title("🛒 Olist E-commerce Analytics Dashboard")
    st.markdown("---")

    # Sidebar
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.selectbox(
        "Choose a view:",
        ["Overview", "Revenue Analysis", "Customer Analysis", "Order Analysis"]
    )

    if page == "Overview":
        show_overview()
    elif page == "Revenue Analysis":
        show_revenue_analysis()
    elif page == "Customer Analysis":
        show_customer_analysis()
    elif page == "Order Analysis":
        show_order_analysis()

def show_overview():
    """Show key metrics overview"""
    st.header("📈 Key Performance Indicators")

    # Load summary metrics
    try:
        # Total metrics
        total_revenue_query = "SELECT SUM(revenue) as total_revenue FROM analytics.monthly_revenue"
        total_customers_query = "SELECT COUNT(DISTINCT customer_id) as total_customers FROM analytics.dim_customer"
        total_orders_query = "SELECT COUNT(DISTINCT order_id) as total_orders FROM analytics.fact_orders"
        avg_order_value_query = "SELECT AVG(total_amount) as avg_order_value FROM analytics.fact_orders WHERE total_amount > 0"

        total_revenue = load_data(total_revenue_query)['total_revenue'].iloc[0]
        total_customers = load_data(total_customers_query)['total_customers'].iloc[0]
        total_orders = load_data(total_orders_query)['total_orders'].iloc[0]
        avg_order_value = load_data(avg_order_value_query)['avg_order_value'].iloc[0]

        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="💰 Total Revenue",
                value=f"R$ {total_revenue:,.2f}" if total_revenue else "R$ 0.00"
            )

        with col2:
            st.metric(
                label="👥 Total Customers",
                value=f"{total_customers:,}" if total_customers else "0"
            )

        with col3:
            st.metric(
                label="📦 Total Orders",
                value=f"{total_orders:,}" if total_orders else "0"
            )

        with col4:
            st.metric(
                label="💵 Avg Order Value",
                value=f"R$ {avg_order_value:.2f}" if avg_order_value else "R$ 0.00"
            )

        st.markdown("---")

        # Quick charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Monthly Revenue Trend")
            monthly_revenue = load_data("SELECT * FROM analytics.monthly_revenue ORDER BY revenue_month")
            if not monthly_revenue.empty:
                fig = px.line(
                    monthly_revenue,
                    x='revenue_month',
                    y='revenue',
                    title="Revenue Over Time"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("🎯 Cancellation Rate")
            cancellation_data = load_data("SELECT * FROM analytics.cancellation_rate ORDER BY cancellation_month")
            if not cancellation_data.empty:
                fig = px.line(
                    cancellation_data,
                    x='cancellation_month',
                    y='cancellation_rate_pct',
                    title="Order Cancellation Rate (%)"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Make sure your database is running and dbt models are built.")

def show_revenue_analysis():
    """Show detailed revenue analysis"""
    st.header("💰 Revenue Analysis")

    try:
        # Monthly revenue
        monthly_revenue = load_data("SELECT * FROM analytics.monthly_revenue ORDER BY revenue_month")

        if not monthly_revenue.empty:
            # Revenue trend
            fig = px.bar(
                monthly_revenue,
                x='revenue_month',
                y='revenue',
                title="Monthly Revenue",
                labels={'revenue': 'Revenue (R$)', 'revenue_month': 'Month'}
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

            # Revenue statistics
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Revenue Statistics")
                st.write(f"**Highest Month:** R$ {monthly_revenue['revenue'].max():,.2f}")
                st.write(f"**Lowest Month:** R$ {monthly_revenue['revenue'].min():,.2f}")
                st.write(f"**Average Monthly:** R$ {monthly_revenue['revenue'].mean():,.2f}")
                st.write(f"**Total Months:** {len(monthly_revenue)}")

            with col2:
                st.subheader("📈 Growth Analysis")
                monthly_revenue['revenue_growth'] = monthly_revenue['revenue'].pct_change() * 100
                avg_growth = monthly_revenue['revenue_growth'].mean()
                st.write(f"**Average Growth Rate:** {avg_growth:.1f}% per month")

                # Show recent trend
                recent_months = monthly_revenue.tail(6)
                if len(recent_months) > 1:
                    recent_growth = recent_months['revenue_growth'].mean()
                    st.write(f"**Recent 6-Month Trend:** {recent_growth:.1f}%")

    except Exception as e:
        st.error(f"Error loading revenue data: {str(e)}")

def show_customer_analysis():
    """Show customer analysis"""
    st.header("👥 Customer Analysis")

    try:
        # Top customers
        top_customers = load_data("SELECT * FROM analytics.top_customers LIMIT 20")

        if not top_customers.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🏆 Top 10 Customers by Spend")
                top_10 = top_customers.head(10)
                fig = px.bar(
                    top_10,
                    x='total_spend',
                    y='customer_city',
                    orientation='h',
                    title="Top Customers by Total Spend",
                    labels={'total_spend': 'Total Spend (R$)', 'customer_city': 'City'}
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("🗺️ Customers by State")
                state_summary = load_data("""
                    SELECT
                        customer_state,
                        COUNT(*) as customer_count,
                        AVG(total_spend) as avg_spend
                    FROM analytics.top_customers
                    GROUP BY customer_state
                    ORDER BY customer_count DESC
                """)

                if not state_summary.empty:
                    fig = px.bar(
                        state_summary.head(10),
                        x='customer_state',
                        y='customer_count',
                        title="Customer Distribution by State",
                        labels={'customer_count': 'Number of Customers', 'customer_state': 'State'}
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)

            # Customer spending distribution
            st.subheader("💵 Customer Spending Distribution")
            fig = px.histogram(
                top_customers,
                x='total_spend',
                nbins=30,
                title="Distribution of Customer Spending",
                labels={'total_spend': 'Total Spend (R$)', 'count': 'Number of Customers'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading customer data: {str(e)}")

def show_order_analysis():
    """Show order analysis"""
    st.header("📦 Order Analysis")

    try:
        # Cancellation analysis
        cancellation_data = load_data("SELECT * FROM analytics.cancellation_rate ORDER BY cancellation_month")

        if not cancellation_data.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📈 Cancellation Rate Trend")
                fig = px.line(
                    cancellation_data,
                    x='cancellation_month',
                    y='cancellation_rate_pct',
                    title="Monthly Cancellation Rate (%)",
                    labels={'cancellation_rate_pct': 'Cancellation Rate (%)', 'cancellation_month': 'Month'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("📊 Order Volume vs Cancellations")
                fig = make_subplots(specs=[[{"secondary_y": True}]])

                fig.add_trace(
                    go.Bar(
                        x=cancellation_data['cancellation_month'],
                        y=cancellation_data['total_orders'],
                        name="Total Orders",
                        marker_color='lightblue'
                    ),
                    secondary_y=False
                )

                fig.add_trace(
                    go.Bar(
                        x=cancellation_data['cancellation_month'],
                        y=cancellation_data['cancelled_orders'],
                        name="Cancelled Orders",
                        marker_color='red'
                    ),
                    secondary_y=False
                )

                fig.update_xaxes(title_text="Month")
                fig.update_yaxes(title_text="Number of Orders", secondary_y=False)
                fig.update_layout(height=400, title="Order Volume Analysis")

                st.plotly_chart(fig, use_container_width=True)

        # Order statistics
        st.subheader("📋 Order Statistics")
        order_stats = load_data("""
            SELECT
                COUNT(*) as total_orders,
                AVG(total_amount) as avg_order_value,
                MIN(total_amount) as min_order_value,
                MAX(total_amount) as max_order_value,
                COUNT(CASE WHEN total_amount > 0 THEN 1 END) as paid_orders
            FROM analytics.fact_orders
        """)

        if not order_stats.empty:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Orders", f"{order_stats['total_orders'].iloc[0]:,}")
                st.metric("Paid Orders", f"{order_stats['paid_orders'].iloc[0]:,}")

            with col2:
                st.metric("Average Order Value", f"R$ {order_stats['avg_order_value'].iloc[0]:.2f}")
                st.metric("Min Order Value", f"R$ {order_stats['min_order_value'].iloc[0]:.2f}")

            with col3:
                st.metric("Max Order Value", f"R$ {order_stats['max_order_value'].iloc[0]:.2f}")
                conversion_rate = (order_stats['paid_orders'].iloc[0] / order_stats['total_orders'].iloc[0]) * 100
                st.metric("Payment Rate", f"{conversion_rate:.1f}%")

    except Exception as e:
        st.error(f"Error loading order data: {str(e)}")

if __name__ == "__main__":
    main()
