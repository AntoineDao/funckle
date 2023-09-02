import React from 'react'
import { Card, List, Space, Typography } from 'antd';
import { RobotOutlined } from '@ant-design/icons'
import { Link } from "react-router-dom";

import { useStreams } from '../../../hooks/useStreams'
import PageColumn from '../../templates/PageColumn';

const StreamList = () => {
    const { streams, loading, error } = useStreams({})

    return (
        <PageColumn
            header={[]}
        >
            <List
                grid={{
                    gutter: 16,
                    column: 4,
                }}
                dataSource={streams}
                loading={loading}
                renderItem={(item) => (
                    <List.Item>
                        <Link to={`/streams/${item.id}`}>
                            <Card
                                loading={loading}
                                cover={<img alt="example" src='https://speckle.systems/content/images/2021/02/automation.png' />}
                                bordered
                                hoverable
                            >
                                <Card.Meta
                                    title={item.name}
                                    description={
                                        <Space>
                                            <Typography.Text>{item.botSet.edges.length} x</Typography.Text>
                                            <RobotOutlined />

                                        </Space>
                                    }
                                />
                            </Card>
                        </Link>

                    </List.Item>
                )}
            />
        </PageColumn>
    )
}

export default StreamList