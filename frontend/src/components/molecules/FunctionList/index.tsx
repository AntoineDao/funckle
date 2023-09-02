import React, { useMemo } from 'react'
import { Button, Card, List, Space, Typography, Row, Col, Avatar } from 'antd';
import { CodeSandboxOutlined } from '@ant-design/icons'
import { Link } from "react-router-dom";

import { useFunctions } from '../../../hooks/useFunctions'
import PageColumn from '../../templates/PageColumn';

const FunctionList = () => {
    const { functions, loading, error } = useFunctions({})

    return (
        <PageColumn
            header={[
                <Link to='/functions/new'>
                    <Button type='primary'>New Function</Button>
                </Link>
            ]}
        >
            <List
                grid={{
                    gutter: 16,
                    column: 2,
                }}
                dataSource={functions}
                loading={loading}
                renderItem={(item) => (
                    <List.Item>
                        <Card
                            loading={loading}
                            bordered
                            hoverable
                        >
                            <Link to={`/functions/${item.id}`}>
                                <Card.Meta
                                    avatar={<Avatar src={item.owner.avatar} />}
                                    title={item.name}
                                    description={(
                                        <Row justify='space-between' align='bottom' gutter={[8, 8]}>
                                            <Col span={24}>
                                                <Space>
                                                    <Typography.Text>{item.functionversionSet ? item.functionversionSet.edges.length : 0} x</Typography.Text>
                                                    <CodeSandboxOutlined />
                                                    <Typography.Text>packages</Typography.Text>
                                                </Space>
                                            </Col>
                                            <Col>
                                                <Typography.Text>{item.description}</Typography.Text>
                                            </Col>
                                        </Row>
                                    )}
                                />
                            </Link>
                        </Card>
                    </List.Item >

                )}
            />
        </PageColumn>
    )
}

export default FunctionList