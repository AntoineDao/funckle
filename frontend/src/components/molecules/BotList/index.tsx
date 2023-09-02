import React from 'react'
import { Card, List, Skeleton } from 'antd';
import { Link, useParams } from "react-router-dom";

import { useStream } from '../../../hooks/useStream'
import BotMeta from '../BotMeta';

type Props = {}

const BotList = (props: Props) => {
    const { streamId } = useParams()
    const { bots, loading, error } = useStream({ id: streamId as string })

    return (
        <List
            grid={{
                gutter: 16,
                column: 1,
            }}
            loading={loading}
            dataSource={bots}
            renderItem={(item) => (
                <List.Item>
                    <Card
                        bordered
                        hoverable
                    >
                        <Link to={`/streams/${streamId}/${item.id}`}>
                            <BotMeta {...item} />
                        </Link>
                    </Card>
                </List.Item>
            )}
        />
    )
}

export default BotList