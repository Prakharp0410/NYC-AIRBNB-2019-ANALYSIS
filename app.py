import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


@st.cache_data

def load_data():
    df = pd.read_csv("D:/PROJECT/PANDAS/data/cleaned_airbnb_2019.csv")
    return df

def add_filters(df):
    """Add filters to the dataframe based on user input from sidebar."""

    st.sidebar.header('🔍 Filter Listings')
    nhoods = df['neighbourhood_group'].unique()
    room_types = df['room_type'].unique()

    selected_nhood = st.sidebar.multiselect("Neighbourhood Group", nhoods, default=list(nhoods))
    selected_room = st.sidebar.multiselect("Room Type", room_types, default=list(room_types))
    price_min, price_max = int(df['price'].min()), int(df['price'].max())
    selected_price = st.sidebar.slider("Price ($)", price_min, price_max, (price_min, min(price_max, 500)))
        
    nights_min, nights_max = int(df['minimum_nights'].min()), int(df['minimum_nights'].max())
    selected_nights = st.sidebar.slider("Minimum Nights", nights_min, min(nights_max, 30), (nights_min, min(nights_max, 7)))
    
    reviews_min, reviews_max = int(df['number_of_reviews'].min()), int(df['number_of_reviews'].max())
    review_count = st.sidebar.slider("Min Number of Reviews", reviews_min, reviews_max, reviews_min)


    filtered = df[
        (df['neighbourhood_group'].isin(selected_nhood)) &
        (df['room_type'].isin(selected_room)) &
        (df['price'].between(*selected_price)) &
        (df['minimum_nights'].between(*selected_nights)) &
        (df['number_of_reviews'] >= review_count)
    ]
    return filtered

def plot_histograms(df):
    """Plot histograms for numeric features in the dataframe."""

    with st.expander("Histograms", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Distribution of Price**")
            fig, ax = plt.subplots()
            ax.hist(df['price'], bins=40, color='skyblue', edgecolor='black')
            ax.set_xlabel('Price ($)')
            ax.set_ylabel('Frequency')
            st.pyplot(fig)
            plt.close(fig)
        with col2:
            st.write("**Distribution of Minimum Nights**")
            fig, ax = plt.subplots()
            ax.hist(df['minimum_nights'], bins=30, color='salmon', edgecolor='black')
            ax.set_xlabel('Minimum Nights')
            ax.set_ylabel('Frequency')
            st.pyplot(fig)
            plt.close(fig)

def plot_barcharts(df):
    """Plot bar charts for categorical features in the dataframe."""

    with st.expander("Bar Charts", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Listings by Neighbourhood Group**")
            nhood_counts = df['neighbourhood_group'].value_counts()
            fig, ax = plt.subplots()
            nhood_counts.plot(kind='bar', color='coral', ax=ax)
            ax.set_ylabel('Count')
            st.pyplot(fig)
            plt.close(fig)
        with col2:
            st.write("**Room Type Counts**")
            room_counts = df['room_type'].value_counts()
            fig, ax = plt.subplots()
            room_counts.plot(kind='bar', color='slateblue', ax=ax)
            ax.set_ylabel('Count')
            st.pyplot(fig)
            plt.close(fig)

def plot_piecharts(df):
    """Plot pie charts for categorical features in the dataframe."""

    with st.expander("Pie Charts", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Share of Room Types**")
            room_share = df['room_type'].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(room_share, labels=room_share.index, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            st.pyplot(fig1)
            plt.close(fig1)
        with col2:
            st.write("**Listings by Neighbourhood Group**")
            nhood_share = df['neighbourhood_group'].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.pie(nhood_share, labels=nhood_share.index, autopct='%1.1f%%', startangle=150)
            plt.axis('equal')
            st.pyplot(fig2)
            plt.tight_layout()
            plt.close(fig2)

def plot_scatter(df):
    """Plot scatter plots for numeric features in the dataframe."""

    with st.expander("Scatter Plot"):
        st.write("**Price vs Number of Reviews**")
        fig, ax = plt.subplots()
        ax.scatter(df['price'], df['number_of_reviews'], alpha=0.5)
        ax.set_xlabel('Price ($)')
        ax.set_ylabel('Number of Reviews')
        st.pyplot(fig)
        plt.close(fig)

def plot_boxplot(df):
    """Plot boxplots for numeric features grouped by categorical features."""

    with st.expander("Boxplot: Price by Neighbourhood Group"):
        fig, ax = plt.subplots()
        df.boxplot(column='price', by='neighbourhood_group', ax=ax)
        plt.title('')
        plt.suptitle('')
        ax.set_xlabel('Neighbourhood Group')
        ax.set_ylabel('Price ($)')
        st.pyplot(fig)
        plt.tight_layout()
        plt.close(fig)

def show_summary_stats(df):
    """Display summary statistics and quick insights about the dataset."""

    st.header("Quick Statistics")
    st.write(f"**Total Listings:** {len(df)}")
    st.write(f"**Average Price:** ${df['price'].mean():.2f}")
    st.write(f"**Median Minimum Nights:** {df['minimum_nights'].median()}")
    st.write(f"**Average Number of Reviews:** {df['number_of_reviews'].mean():.1f}")
    st.write(f"**Earliest Review Date:** {df['last_review'].min() if 'last_review' in df else 'N/A'}")

def plot_heatmap(df):
    """Plot a correlation heatmap for numeric features in the dataframe."""

    with st.expander("Correlation Heatmap (Matplotlib only)", expanded=True):
        st.write("**Correlation Heatmap of Numeric Features**")
        numeric_df = df.select_dtypes(include=[np.number])
        corr = numeric_df.corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        cax = ax.matshow(corr, cmap='coolwarm')
        fig.colorbar(cax)

        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha='left')
        ax.set_yticklabels(corr.columns)

        for i in range(len(corr.columns)):
            for j in range(len(corr.columns)):
                ax.text(j, i, f'{corr.iloc[i, j]:.2f}', va='center', ha='center', color='black')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


st.title("NYC Airbnb 2019 – Data Explorer")
df = load_data()

st.write("Top 5 listings based on number of reviews:")
st.dataframe(df.sort_values(by='number_of_reviews', ascending=False).head(),
                 use_container_width=True)

df_filtered = add_filters(df)
if df_filtered.empty:
    st.warning("No listings match the selected filters. Adjust your filters to see data and visualizations.")
    st.stop()

st.write(f"### Filtered Data Preview (Showing top 5 of {len(df_filtered)} rows)")
st.dataframe(df_filtered.head(), use_container_width=True)

show_summary_stats(df_filtered)
plot_histograms(df_filtered)
plot_barcharts(df_filtered)
plot_piecharts(df_filtered)
plot_scatter(df_filtered)
plot_boxplot(df_filtered)
plot_heatmap(df_filtered)

with st.expander("Raw Data Sample"):
    st.dataframe(df_filtered.sample(min(len(df_filtered), 20)), use_container_width=True)


if __name__ == "__main__":
    pass
