"""Case-derived evidence figure templates.

These functions encode argument structure learned from reviewed excellent papers.
They do not copy a paper's exact palette and never turn synthetic/demo results into evidence.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def _save(fig, out_path, tight=True):
    out=Path(out_path); out.parent.mkdir(parents=True,exist_ok=True)
    if tight:
        fig.tight_layout()
    fig.savefig(out,dpi=300,bbox_inches='tight'); plt.close(fig)
    return str(out)


def paired_embedding(before, after, before_labels, after_labels, out_path,
                     before_title='Before adaptation', after_title='After adaptation'):
    """Two-panel embedding comparison. Visual mixing is NOT target accuracy."""
    before=np.asarray(before); after=np.asarray(after)
    fig,axes=plt.subplots(1,2,figsize=(9,4),sharex=False,sharey=False)
    for ax,x,y,title in [(axes[0],before,before_labels,before_title),(axes[1],after,after_labels,after_title)]:
        y=np.asarray(y)
        for lab in np.unique(y):
            m=y==lab; ax.scatter(x[m,0],x[m,1],s=14,label=str(lab),alpha=.75)
        ax.set_title(title); ax.set_xlabel('Embedding 1'); ax.set_ylabel('Embedding 2'); ax.grid(alpha=.18)
    handles,labels=axes[1].get_legend_handles_labels()
    if handles: axes[1].legend(handles,labels,fontsize=8,frameon=False)
    return _save(fig,out_path)


def confusion_grid(matrices, class_names, titles, out_path):
    """Aligned confusion matrices with shared numeric scale."""
    mats=[np.asarray(m) for m in matrices]; vmax=max(float(m.max()) for m in mats) if mats else 1
    fig,axes=plt.subplots(1,len(mats),figsize=(4.2*len(mats)+.7,3.8),squeeze=False,layout='constrained')
    for ax,m,title in zip(axes[0],mats,titles):
        im=ax.imshow(m,vmin=0,vmax=vmax,aspect='equal')
        ax.set_title(title); ax.set_xticks(range(len(class_names)),class_names); ax.set_yticks(range(len(class_names)),class_names)
        ax.set_xlabel('Predicted'); ax.set_ylabel('True')
        for i in range(m.shape[0]):
            for j in range(m.shape[1]): ax.text(j,i,f'{m[i,j]:g}',ha='center',va='center',fontsize=8)
    fig.colorbar(im,ax=axes.ravel().tolist(),fraction=.035,pad=.03)
    return _save(fig,out_path,tight=False)


def repeated_metric_boxplot(metric_runs, out_path, ylabel='Metric'):
    """Repeated-run stability, complementary to one best accuracy."""
    names=list(metric_runs); vals=[np.asarray(metric_runs[n],dtype=float) for n in names]
    fig,ax=plt.subplots(figsize=(7,4)); ax.boxplot(vals,labels=names,showmeans=True)
    ax.set_ylabel(ylabel); ax.set_title('Repeated-run stability'); ax.grid(axis='y',alpha=.2)
    return _save(fig,out_path)


def target_probability_heatmap(probabilities, sample_names, class_names, out_path):
    """Unlabeled target probability display. Confidence/probability is NOT accuracy."""
    p=np.asarray(probabilities,dtype=float)
    fig,ax=plt.subplots(figsize=(max(7,.48*len(sample_names)),4.5)); im=ax.imshow(p.T,aspect='auto',vmin=0,vmax=1)
    ax.set_xticks(range(len(sample_names)),sample_names,rotation=60,ha='right'); ax.set_yticks(range(len(class_names)),class_names)
    ax.set_xlabel('Target sample'); ax.set_ylabel('Predicted class'); ax.set_title('Target predicted probabilities (not accuracy)')
    fig.colorbar(im,ax=ax,label='Predicted probability')
    return _save(fig,out_path)


def signal_mechanism_four_panel(t, raw, reconstructed, freq, spectrum, env_freq, env_spectrum, out_path):
    """Four-panel mechanism/effect figure for the same signal object."""
    t=np.asarray(t); raw=np.asarray(raw); reconstructed=np.asarray(reconstructed)
    fig,axes=plt.subplots(2,2,figsize=(9,6))
    axes[0,0].plot(t,raw,label='Raw',linewidth=.9); axes[0,0].plot(t,reconstructed,label='Reconstructed',linewidth=.9)
    axes[0,0].set_title('Raw vs reconstructed'); axes[0,0].set_xlabel('Time'); axes[0,0].legend(frameon=False,fontsize=8)
    residual=raw-reconstructed; axes[0,1].plot(t,residual,linewidth=.9); axes[0,1].set_title('Residual / removed component'); axes[0,1].set_xlabel('Time')
    axes[1,0].plot(freq,spectrum,linewidth=.9); axes[1,0].set_title('Spectrum'); axes[1,0].set_xlabel('Frequency')
    axes[1,1].plot(env_freq,env_spectrum,linewidth=.9); axes[1,1].set_title('Envelope spectrum'); axes[1,1].set_xlabel('Frequency')
    for ax in axes.ravel(): ax.grid(alpha=.18)
    return _save(fig,out_path)


def prediction_curve_parity(y_true, y_pred, split_index, out_path, x=None):
    """Chronological prediction evidence: time curve plus parity scatter, split shown explicitly."""
    y_true=np.asarray(y_true,dtype=float); y_pred=np.asarray(y_pred,dtype=float)
    if y_true.shape!=y_pred.shape: raise ValueError('y_true and y_pred must have same shape')
    if not 1<=int(split_index)<len(y_true): raise ValueError('split_index must be inside series')
    x=np.arange(len(y_true)) if x is None else np.asarray(x)
    fig,axes=plt.subplots(1,2,figsize=(9,4))
    axes[0].plot(x,y_true,label='Observed',linewidth=.9); axes[0].plot(x,y_pred,label='Predicted',linewidth=.9)
    axes[0].axvline(x[int(split_index)],linestyle='--',linewidth=.9,label='Train/test boundary')
    axes[0].set_title('Chronological prediction'); axes[0].set_xlabel('Time / ordered sample'); axes[0].legend(frameon=False,fontsize=8)
    tr=slice(0,int(split_index)); te=slice(int(split_index),None)
    axes[1].scatter(y_true[tr],y_pred[tr],s=12,alpha=.6,label='Train'); axes[1].scatter(y_true[te],y_pred[te],s=12,alpha=.75,label='Test')
    lo=float(min(y_true.min(),y_pred.min())); hi=float(max(y_true.max(),y_pred.max())); axes[1].plot([lo,hi],[lo,hi],linestyle='--',linewidth=.9)
    axes[1].set_xlim(lo,hi); axes[1].set_ylim(lo,hi); axes[1].set_title('Parity by split'); axes[1].set_xlabel('Observed'); axes[1].set_ylabel('Predicted'); axes[1].legend(frameon=False,fontsize=8)
    for ax in axes: ax.grid(alpha=.18)
    return _save(fig,out_path)


def constraint_validation_dashboard(values, lower, upper, total_target, out_path, center=None, center_tolerance=None):
    """Validate aggregate balance and componentwise feasibility separately."""
    v=np.asarray(values,dtype=float)
    if v.ndim!=2: raise ValueError('values must be time x entity')
    T,N=v.shape
    lo=np.broadcast_to(np.asarray(lower,dtype=float),v.shape); hi=np.broadcast_to(np.asarray(upper,dtype=float),v.shape)
    tgt=np.asarray(total_target,dtype=float).reshape(-1)
    if len(tgt)!=T: raise ValueError('total_target length mismatch')
    below=np.maximum(lo-v,0); above=np.maximum(v-hi,0); viol=np.maximum(below,above)
    if center is not None and center_tolerance is not None:
        c=np.broadcast_to(np.asarray(center,dtype=float),v.shape); tol=np.broadcast_to(np.asarray(center_tolerance,dtype=float),v.shape)
        viol=np.maximum(viol,np.maximum(np.abs(v-c)-tol,0))
    count=(viol>0).sum(axis=1); vmax=viol.max(axis=1); agg=v.sum(axis=1)-tgt
    fig,axes=plt.subplots(3,1,figsize=(8,7),sharex=True)
    axes[0].plot(tgt,label='Target total',linewidth=.9); axes[0].plot(v.sum(axis=1),label='Allocated total',linewidth=.9); axes[0].legend(frameon=False,fontsize=8); axes[0].set_ylabel('Total'); axes[0].set_title('Aggregate balance')
    axes[1].plot(agg,linewidth=.9); axes[1].axhline(0,linestyle='--',linewidth=.8); axes[1].set_ylabel('Total error'); axes[1].set_title('Aggregate error')
    axes[2].plot(count,label='Violation count',linewidth=.9); axes[2].plot(vmax,label='Max violation magnitude',linewidth=.9); axes[2].set_ylabel('Violation'); axes[2].set_xlabel('Time'); axes[2].set_title('Componentwise feasibility'); axes[2].legend(frameon=False,fontsize=8)
    for ax in axes: ax.grid(alpha=.18)
    return _save(fig,out_path)



def pareto_front_operating_point(objective_a, objective_b, selected_index, out_path,
                                 xlabel='Objective 1', ylabel='Objective 2'):
    """Show the actual Pareto trade-off and make the final operating-point decision explicit."""
    a=np.asarray(objective_a,dtype=float).reshape(-1); b=np.asarray(objective_b,dtype=float).reshape(-1)
    if len(a)!=len(b) or len(a)<2: raise ValueError('objective arrays must have same length >=2')
    idx=int(selected_index)
    if not 0<=idx<len(a): raise ValueError('selected_index out of range')
    order=np.argsort(a)
    fig,ax=plt.subplots(figsize=(6.5,4.5))
    ax.plot(a[order],b[order],marker='o',markersize=3,linewidth=.9,label='Candidate trade-off')
    ax.scatter([a[idx]],[b[idx]],s=70,marker='*',label='Selected operating point',zorder=4)
    ax.annotate('selected',xy=(a[idx],b[idx]),xytext=(8,8),textcoords='offset points')
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_title('Pareto trade-off and operating-point selection')
    ax.legend(frameon=False,fontsize=8); ax.grid(alpha=.18)
    return _save(fig,out_path)


def robustness_severity_curve(severity, methods, out_path, ylabel='Downstream metric'):
    """Robustness evidence across a severity sweep; one corrupted test condition is insufficient."""
    sev=np.asarray(severity,dtype=float).reshape(-1)
    fig,ax=plt.subplots(figsize=(7,4.5))
    for name,vals in methods.items():
        y=np.asarray(vals,dtype=float).reshape(-1)
        if len(y)!=len(sev): raise ValueError(f'length mismatch for {name}')
        ax.plot(sev,y,marker='o',markersize=3,linewidth=.9,label=str(name))
    ax.set_xlabel('Noise / delay severity'); ax.set_ylabel(ylabel); ax.set_title('Robustness across corruption severity')
    ax.legend(frameon=False,fontsize=8); ax.grid(alpha=.18)
    return _save(fig,out_path)


def runtime_latency_distribution(latencies, deadline, out_path, label='Method'):
    """Real-time evidence should show latency distribution/high quantiles, not only batch throughput."""
    x=np.asarray(latencies,dtype=float).reshape(-1)
    if len(x)<2: raise ValueError('latencies must contain at least two steps')
    xs=np.sort(x); ecdf=np.arange(1,len(xs)+1)/len(xs)
    q50,q95,q99=np.quantile(x,[.5,.95,.99])
    fig,axes=plt.subplots(1,2,figsize=(9,4))
    axes[0].plot(xs,ecdf,linewidth=.9,label=label); axes[0].axvline(float(deadline),linestyle='--',linewidth=.9,label='Deadline')
    axes[0].set_xlabel('Per-step latency'); axes[0].set_ylabel('ECDF'); axes[0].set_title('Online latency distribution'); axes[0].legend(frameon=False,fontsize=8)
    axes[1].bar(['P50','P95','P99','Max'],[q50,q95,q99,x.max()]); axes[1].axhline(float(deadline),linestyle='--',linewidth=.9,label='Deadline')
    axes[1].set_ylabel('Latency'); axes[1].set_title('High-quantile / worst-case latency'); axes[1].legend(frameon=False,fontsize=8)
    for ax in axes: ax.grid(axis='y',alpha=.18)
    return _save(fig,out_path)


def multi_metric_tradeoff(method_metrics, metric_directions, out_path):
    """Direction-aware multi-metric comparison. A method is not an overall winner if one key metric worsens."""
    methods=list(method_metrics)
    metrics=list(metric_directions)
    raw=np.asarray([[float(method_metrics[m][k]) for k in metrics] for m in methods],dtype=float)
    score=np.zeros_like(raw)
    for j,k in enumerate(metrics):
        col=raw[:,j]; lo=float(col.min()); hi=float(col.max()); den=hi-lo if hi>lo else 1.0
        norm=(col-lo)/den
        direction=str(metric_directions[k]).lower()
        if direction in {'min','lower','smaller'}: norm=1-norm
        elif direction not in {'max','higher','larger'}: raise ValueError(f'unknown direction for {k}: {metric_directions[k]}')
        score[:,j]=norm
    fig,ax=plt.subplots(figsize=(max(7,.9*len(metrics)+3),max(3.8,.55*len(methods)+2)))
    im=ax.imshow(score,aspect='auto',vmin=0,vmax=1)
    ax.set_xticks(range(len(metrics)),metrics,rotation=35,ha='right'); ax.set_yticks(range(len(methods)),methods)
    ax.set_title('Direction-aware metric trade-off (normalized for display only)')
    for i in range(len(methods)):
        for j in range(len(metrics)):
            ax.text(j,i,f'{raw[i,j]:.3g}',ha='center',va='center',fontsize=8)
    fig.colorbar(im,ax=ax,label='Direction-aware display score')
    return _save(fig,out_path)


def cascade_oof_validation(y_true, direct_pred, oracle_stage2_pred, cascade_pred, out_path):
    """Compare direct, oracle-stage2, and true end-to-end cascade errors.

    The oracle-stage2 curve is diagnostic only: it uses ground-truth intermediates and must not
    be reported as deployed cascade performance when deployment receives stage-1 predictions.
    """
    y=np.asarray(y_true,dtype=float).reshape(-1)
    preds={
        'Direct baseline':np.asarray(direct_pred,dtype=float).reshape(-1),
        'Stage 2 with true intermediates':np.asarray(oracle_stage2_pred,dtype=float).reshape(-1),
        'End-to-end OOF cascade':np.asarray(cascade_pred,dtype=float).reshape(-1),
    }
    if any(len(v)!=len(y) for v in preds.values()):
        raise ValueError('all prediction arrays must match y_true length')
    fig,axes=plt.subplots(1,2,figsize=(10,4.2))
    lo=min([float(y.min())]+[float(v.min()) for v in preds.values()]); hi=max([float(y.max())]+[float(v.max()) for v in preds.values()])
    for name,p in preds.items():
        axes[0].scatter(y,p,s=12,alpha=.6,label=name)
    axes[0].plot([lo,hi],[lo,hi],linestyle='--',linewidth=.9)
    axes[0].set_xlabel('Observed'); axes[0].set_ylabel('Predicted'); axes[0].set_title('Oracle vs deployed cascade')
    axes[0].legend(frameon=False,fontsize=7)
    names=list(preds); maes=[float(np.mean(np.abs(preds[n]-y))) for n in names]
    axes[1].barh(names,maes); axes[1].set_xlabel('MAE'); axes[1].set_title('End-to-end error must be reported')
    for ax in axes: ax.grid(alpha=.18)
    return _save(fig,out_path)


def resampling_partition_diagnostic(train_labels, valid_labels, resampled_train_labels, out_path):
    """Show class balance before/after TRAIN-ONLY resampling while validation stays natural."""
    tr=np.asarray(train_labels); va=np.asarray(valid_labels); rr=np.asarray(resampled_train_labels)
    classes=np.unique(np.concatenate([tr,va,rr]))
    def counts(a): return np.array([(a==c).sum() for c in classes],dtype=float)
    x=np.arange(len(classes)); width=.26
    fig,ax=plt.subplots(figsize=(max(7,.55*len(classes)+3),4.5))
    ax.bar(x-width,counts(tr),width,label='Train before resampling')
    ax.bar(x,counts(rr),width,label='Train after resampling')
    ax.bar(x+width,counts(va),width,label='Validation (untouched)')
    ax.set_xticks(x,[str(c) for c in classes],rotation=45,ha='right')
    ax.set_ylabel('Sample count'); ax.set_xlabel('Class'); ax.set_title('Resample training only; keep validation natural')
    ax.legend(frameon=False,fontsize=8); ax.grid(axis='y',alpha=.18)
    return _save(fig,out_path)


def imbalanced_classification_dashboard(y_true, y_pred, out_path, class_labels=None):
    """Expose majority-class accuracy inflation with confusion counts and per-class metrics."""
    from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score, balanced_accuracy_score
    y=np.asarray(y_true); p=np.asarray(y_pred)
    if y.shape!=p.shape: raise ValueError('y_true and y_pred must have same shape')
    labels=np.unique(np.concatenate([y,p])) if class_labels is None else np.asarray(class_labels)
    cm=confusion_matrix(y,p,labels=labels)
    pr,rc,f1,sup=precision_recall_fscore_support(y,p,labels=labels,zero_division=0)
    acc=float(accuracy_score(y,p)); bacc=float(balanced_accuracy_score(y,p)); macro=float(np.mean(f1))
    fig,axes=plt.subplots(1,2,figsize=(10,4.5))
    im=axes[0].imshow(cm,aspect='auto')
    axes[0].set_xticks(range(len(labels)),[str(x) for x in labels],rotation=45,ha='right')
    axes[0].set_yticks(range(len(labels)),[str(x) for x in labels])
    axes[0].set_xlabel('Predicted'); axes[0].set_ylabel('True'); axes[0].set_title('Confusion counts')
    for i in range(len(labels)):
        for j in range(len(labels)): axes[0].text(j,i,str(int(cm[i,j])),ha='center',va='center',fontsize=8)
    fig.colorbar(im,ax=axes[0],fraction=.046,pad=.04)
    x=np.arange(len(labels)); w=.24
    axes[1].bar(x-w,pr,w,label='Precision'); axes[1].bar(x,rc,w,label='Recall'); axes[1].bar(x+w,f1,w,label='F1')
    axes[1].set_xticks(x,[f'{lab}\nn={int(n)}' for lab,n in zip(labels,sup)],rotation=45,ha='right')
    axes[1].set_ylim(0,1.05); axes[1].set_ylabel('Score'); axes[1].set_title(f'Accuracy={acc:.3f} | Balanced={bacc:.3f} | Macro F1={macro:.3f}')
    axes[1].legend(frameon=False,fontsize=8); axes[1].grid(axis='y',alpha=.18)
    return _save(fig,out_path)


def structured_pair_validity(true_a, true_b, pred_a, pred_b, valid_pairs, out_path, a_name='Output A', b_name='Output B'):
    """Audit independently predicted structured labels against the allowed tuple set."""
    ta=np.asarray(true_a); tb=np.asarray(true_b); pa=np.asarray(pred_a); pb=np.asarray(pred_b)
    if not (ta.shape==tb.shape==pa.shape==pb.shape): raise ValueError('all arrays must have same shape')
    valid={tuple(x) for x in valid_pairs}
    pairs=list(zip(pa.tolist(),pb.tolist()))
    bad=np.array([x not in valid for x in pairs],dtype=bool)
    exact=(pa==ta)&(pb==tb)
    # counts on supported pair grid
    all_a=sorted({x[0] for x in valid}|set(pa.tolist())); all_b=sorted({x[1] for x in valid}|set(pb.tolist()))
    ai={v:i for i,v in enumerate(all_a)}; bi={v:i for i,v in enumerate(all_b)}
    counts=np.zeros((len(all_a),len(all_b)),dtype=int)
    for a,b in pairs: counts[ai[a],bi[b]]+=1
    fig,axes=plt.subplots(1,2,figsize=(10,4.5))
    im=axes[0].imshow(counts,aspect='auto')
    axes[0].set_yticks(range(len(all_a)),[str(x) for x in all_a]); axes[0].set_xticks(range(len(all_b)),[str(x) for x in all_b],rotation=45,ha='right')
    axes[0].set_ylabel(a_name); axes[0].set_xlabel(b_name); axes[0].set_title('Predicted tuple counts')
    for i,a in enumerate(all_a):
        for j,b in enumerate(all_b):
            txt=str(counts[i,j])
            if (a,b) not in valid: txt += ' ×'
            axes[0].text(j,i,txt,ha='center',va='center',fontsize=8)
    fig.colorbar(im,ax=axes[0],fraction=.046,pad=.04)
    vals=[float(np.mean(pa==ta)),float(np.mean(pb==tb)),float(np.mean(exact)),float(np.mean(bad))]
    axes[1].bar(['A marginal\naccuracy','B marginal\naccuracy','Joint exact\nmatch','Invalid tuple\nrate'],vals)
    axes[1].set_ylim(0,1.05); axes[1].set_ylabel('Rate'); axes[1].set_title('Marginal scores do not imply valid joint output')
    axes[1].grid(axis='y',alpha=.18)
    return _save(fig,out_path)


def adjusted_interaction_plot(x_levels, group_series, ci_series, out_path, xlabel='Factor A', ylabel='Adjusted response'):
    """Interaction evidence using adjusted means and confidence intervals, not raw group means alone."""
    x=np.arange(len(x_levels),dtype=float)
    fig,ax=plt.subplots(figsize=(7.2,4.6))
    for name,vals in group_series.items():
        y=np.asarray(vals,dtype=float).reshape(-1)
        if len(y)!=len(x): raise ValueError(f'length mismatch for {name}')
        ci=np.asarray(ci_series[name],dtype=float)
        if ci.ndim==1:
            if len(ci)!=len(x): raise ValueError(f'CI length mismatch for {name}')
            yerr=ci
        elif ci.shape==(2,len(x)):
            yerr=ci
        else: raise ValueError(f'CI shape mismatch for {name}')
        ax.errorbar(x,y,yerr=yerr,marker='o',linewidth=.9,capsize=3,label=str(name))
    ax.set_xticks(x,[str(v) for v in x_levels]); ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.set_title('Covariate-adjusted interaction with uncertainty'); ax.legend(frameon=False,fontsize=8); ax.grid(alpha=.18)
    return _save(fig,out_path)


def optimization_feasibility_audit(variable_names, bounds, reported_points, out_path):
    """Normalize reported optima to declared bounds and make violations visible before publication."""
    names=list(variable_names)
    if len(bounds)!=len(names): raise ValueError('bounds length mismatch')
    lo=np.array([float(b[0]) for b in bounds]); hi=np.array([float(b[1]) for b in bounds])
    if np.any(hi<=lo): raise ValueError('each upper bound must exceed lower bound')
    fig,ax=plt.subplots(figsize=(max(7,.9*len(names)+3),4.6))
    x=np.arange(len(names))
    ax.axhspan(0,1,alpha=.08,label='Declared feasible interval')
    for label,vals in reported_points.items():
        v=np.asarray(vals,dtype=float).reshape(-1)
        if len(v)!=len(names): raise ValueError(f'point length mismatch for {label}')
        z=(v-lo)/(hi-lo)
        ax.plot(x,z,marker='o',linewidth=.9,label=str(label))
    ax.axhline(0,linestyle='--',linewidth=.8); ax.axhline(1,linestyle='--',linewidth=.8)
    ax.set_xticks(x,names,rotation=25,ha='right'); ax.set_ylabel('Normalized position: 0=lower, 1=upper')
    ax.set_title('Reported optimum feasibility replay'); ax.legend(frameon=False,fontsize=8); ax.grid(axis='y',alpha=.18)
    return _save(fig,out_path)


def categorical_encoder_contract_matrix(categories, encoded_vectors, out_path, title='Categorical encoder contract'):
    """Visualize the exact inference encoder so all-zero/invalid category encodings are obvious."""
    cats=[str(x) for x in categories]
    mat=np.asarray(encoded_vectors,dtype=float)
    if mat.ndim!=2 or mat.shape[0]!=len(cats): raise ValueError('encoded_vectors must be rows aligned to categories')
    fig,ax=plt.subplots(figsize=(max(6,.65*mat.shape[1]+3),max(3.8,.45*len(cats)+2)))
    im=ax.imshow(mat,aspect='auto')
    ax.set_yticks(range(len(cats)),cats); ax.set_xticks(range(mat.shape[1]),[f'bit {i}' for i in range(mat.shape[1])])
    ax.set_xlabel('Encoded feature'); ax.set_ylabel('Legal category'); ax.set_title(title)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]): ax.text(j,i,f'{mat[i,j]:.0f}',ha='center',va='center',fontsize=8)
    zero_rows=np.where(np.sum(np.abs(mat),axis=1)==0)[0]
    if len(zero_rows): ax.text(.01,-.16,f'All-zero legal categories: {", ".join(cats[i] for i in zero_rows)}',transform=ax.transAxes,fontsize=8)
    fig.colorbar(im,ax=ax,fraction=.046,pad=.04)
    return _save(fig,out_path)


def scalarization_sensitivity_plot(objective_a, objective_b, labels, out_path, n_weights=41):
    """Show how raw vs min-max-normalized weighted sums select different candidates as preference changes."""
    a=np.asarray(objective_a,dtype=float).reshape(-1); b=np.asarray(objective_b,dtype=float).reshape(-1)
    labels=[str(x) for x in labels]
    if not (len(a)==len(b)==len(labels)): raise ValueError('objective arrays and labels must align')
    def norm(x):
        lo=float(x.min()); hi=float(x.max()); return (x-lo)/(hi-lo if hi>lo else 1.0)
    an,bn=norm(a),norm(b)
    ws=np.linspace(0,1,int(n_weights))
    raw=[]; normalized=[]
    for w in ws:
        raw.append(int(np.argmin(w*a+(1-w)*b)))
        normalized.append(int(np.argmin(w*an+(1-w)*bn)))
    fig,axes=plt.subplots(2,1,figsize=(8,5.2),sharex=True)
    axes[0].step(ws,raw,where='mid'); axes[0].set_ylabel('Selected candidate'); axes[0].set_yticks(range(len(labels)),labels); axes[0].set_title('Raw-scale weighted sum')
    axes[1].step(ws,normalized,where='mid'); axes[1].set_ylabel('Selected candidate'); axes[1].set_yticks(range(len(labels)),labels); axes[1].set_title('Normalized-objective weighted sum'); axes[1].set_xlabel('Weight on objective A')
    for ax in axes: ax.grid(alpha=.18)
    fig.suptitle('Scalarization sensitivity: equal weights do not mean equal preference across units',fontsize=10)
    return _save(fig,out_path)
