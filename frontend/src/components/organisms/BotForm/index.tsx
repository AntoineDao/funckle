import React from 'react'
import { Button, Form, Input, Select, SelectProps, Space, Divider, notification } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';

import SelectFunctionVersion from '../../molecules/SelectFunctionVersion';
import { useFunctions } from '../../../hooks/useFunctions'

const formItemLayout = {
    labelCol: {
        xs: { span: 24 },
        sm: { span: 8 },
    },
    wrapperCol: {
        xs: { span: 24 },
        sm: { span: 16 },
    },
};

const tailFormItemLayout = {
    wrapperCol: {
        xs: {
            span: 24,
            offset: 0,
        },
        sm: {
            span: 16,
            offset: 8,
        },
    },
};

const TRIGGER_OPTIONS: SelectProps['options'] = [
    { label: 'Branch Create', value: 'branch_create' },
    { label: 'Branch Delete', value: 'branch_delete' },
    { label: 'Branch Update', value: 'branch_update' },
    { label: 'Commit Create', value: 'commit_create' },
    { label: 'Commit Delete', value: 'commit_delete' },
    { label: 'Commit Update', value: 'commit_update' },
    { label: 'Stream Delete', value: 'stream_delete' },
    { label: 'Stream Update', value: 'stream_update' },
    { label: 'Commit Receive', value: 'commit_receive' },
    { label: 'Comment Created', value: 'comment_created' },
    { label: 'Comment Replied', value: 'comment_replied' },
    { label: 'Comment Archived', value: 'comment_archived' },
    { label: 'Stream Permissions Add', value: 'stream_permissions_add' },
    { label: 'Stream Permissions Remove', value: 'stream_permissions_remove' },
]

type EnvironmentVariable = {
    name: string
    value: string
}

type InitialValues = {
    slug?: string,
    description?: string,
    functionVersionId?: string
    triggers?: string[]
    environmentVariables?: EnvironmentVariable[]
    secretEnvironmentVariables?: EnvironmentVariable[]
}


type EnvVarFormProps = {
    name: string
    initialValues?: EnvironmentVariable[]
}

export const EnvVarForm = (props: EnvVarFormProps) => {
    const cleanInitialValues = props.initialValues?.map((envVar) => ({ name: envVar.name, value: envVar.value })) ?? []

    return (
        <Form.List name={props.name} initialValue={cleanInitialValues}>
            {(fields, { add, remove }) => (
                <>
                    {fields.map(({ key, name, ...restField }) => (
                        <Space key={key} style={{ display: 'flex', marginBottom: 8 }} align="baseline">
                            <Form.Item
                                {...restField}
                                name={[name, 'name']}
                                rules={[{ required: true, message: 'Missing variable name' }]}
                            >
                                <Input placeholder="Name" />
                            </Form.Item>
                            <Form.Item
                                {...restField}
                                name={[name, 'value']}
                                rules={[{ required: true, message: 'Missing variable value' }]}
                            >
                                <Input placeholder="Value" />
                            </Form.Item>
                            <MinusCircleOutlined onClick={() => remove(name)} />
                        </Space>
                    ))}
                    <Form.Item>
                        <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                            Add field
                        </Button>
                    </Form.Item>
                </>
            )}
        </Form.List>


    )
}

type BotFormValues = {
    slug: string,
    description: string,
    functionVersionId: string
    triggers: string[]
    environmentVariables: EnvironmentVariable[]
    secretEnvironmentVariables: EnvironmentVariable[]
}

type Props = {
    initialValues?: InitialValues,
    buttonText: string,
    onFinish(values: BotFormValues): Promise<void>
}

const BotForm = (props: Props) => {
    const [form] = Form.useForm();

    const { functions, loading, error } = useFunctions({})

    const [formLoading, setFormLoading] = React.useState(false)

    const onSubmit = (values: any) => {
        setFormLoading(true)
        props.onFinish(values).finally(() => {
            setFormLoading(false)
        })
    };


    return (
        <Form
            {...formItemLayout}
            form={form}
            name="function"
            onFinish={onSubmit}
            initialValues={props.initialValues}
            style={{ maxWidth: 800 }}
        >
            <Form.Item
                name="slug"
                label="Name"
                rules={[{ required: true, message: 'name is required' }]}
            >
                <Input />
            </Form.Item>
            <Form.Item
                name="description"
                label="Description"
                initialValue={props.initialValues?.description ?? ""}
            >
                <Input.TextArea showCount maxLength={100} />
            </Form.Item>
            <Form.Item
                name="functionVersionId"
                label="Function Version"
                rules={[{ required: true, message: 'Funtion version is required' }]}
            >
                <SelectFunctionVersion
                    functions={functions}
                    initialFunctionVersionId={props.initialValues?.functionVersionId}
                    selectFunctionVersion={(value?: string) => {
                        form.setFieldsValue({ functionVersionId: value })
                    }}
                />
            </Form.Item>
            <Form.Item
                name="triggers"
                label="Triggers"
                initialValue={props.initialValues?.triggers ?? []}
                rules={[{ required: true, message: 'Bot triggers version are required' }]}
            >
                <Select
                    mode="multiple"
                    allowClear
                    placeholder="Please select at least one trigger"
                    defaultValue={props.initialValues?.triggers}
                    options={TRIGGER_OPTIONS}
                />
            </Form.Item>
            <Divider />
            <Form.Item
                label="Environment Config"
            >
                <EnvVarForm name="environmentVariables" initialValues={props.initialValues?.environmentVariables ?? []} />
            </Form.Item>
            <Form.Item
                label="Environment Secrets"
            >
                <EnvVarForm name="secretEnvironmentVariables" initialValues={props.initialValues?.secretEnvironmentVariables ?? []} />
            </Form.Item>
            <Form.Item {...tailFormItemLayout}>
                <Button loading={formLoading} type="primary" htmlType="submit">
                    {props.buttonText}
                </Button>
            </Form.Item>
        </Form>
    );

}

export default BotForm