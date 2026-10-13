
import pandas as pd 


def allocate_direct_costs(df):
    direct_df = df[df["allocation_type"] == "Direct"].copy()
    direct_df["allocated_amount"] = (direct_df["amount"])
    direct_df = direct_df.drop(columns="amount")
    return direct_df

def allocate_by_headcount(shared_df, headcount_df):

    result = []

    for _, cost in shared_df.iterrows():

        period = cost["period"]

        period_headcount = headcount_df[
            headcount_df["period"] == period
        ]

        total_headcount = (
            period_headcount["headcount"]
            .sum()
        )


        for _, company in period_headcount.iterrows():

            allocated_amount = (
                cost["amount"]
                *
                company["headcount"]
                /
                total_headcount
            )


            result.append({

                "company": company["company"],
                "cost_title": cost["cost_title"],
                "period": period,
                "allocated_amount": allocated_amount,
                "allocation_type": "Shared_Headcount"

            })


    return pd.DataFrame(result)


def allocate_costs(cost_df, headcount_df):

    direct = allocate_direct_costs(cost_df)


    shared_headcount = cost_df[
        cost_df["allocation_type"]
        ==
        "Shared_Headcount"
    ]


    allocated_shared = allocate_by_headcount(
        shared_headcount,
        headcount_df
    )


    final_df = pd.concat(
        [
            direct,
            allocated_shared
        ],
        ignore_index=True
    )
    
    final_df["allocated_amount"] = (
        final_df["allocated_amount"]
        .fillna(0)
    )


    return final_df