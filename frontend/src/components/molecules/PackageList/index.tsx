import React, { useMemo } from 'react'
import { Card, List, Skeleton, Space, Typography } from 'antd';
import { Link } from "react-router-dom";

import { FunctionVersion } from '../../../hooks/useFunction';
import PackageMeta from '../PackageMeta';

type Props = {
    functionId: string
    packages?: Array<FunctionVersion>
}

const PackageList = (props: Props) => {

    const loading = useMemo(() => {
        return props.packages === undefined
    }, [props.packages])


    return (
        <List
            grid={{
                gutter: 16,
                column: 1,
            }}
            // @ts-ignore
            dataSource={!loading ? props.packages : [{}, {}, {}]}
            renderItem={(item) => (
                <List.Item>
                    <Card
                        bordered
                        hoverable
                    >
                        {/* @ts-ignore */}
                        <Skeleton loading={loading} avatar paragraph={{ rows: 0 }}>
                            <Link to={`/functions/${props.functionId}/${item.id}`}>
                                <PackageMeta {...item} />
                            </Link>
                        </Skeleton>
                    </Card>
                </List.Item>
            )}
        />
    )
}

export default PackageList